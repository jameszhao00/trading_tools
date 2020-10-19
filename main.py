from dataclasses import dataclass
from datetime import datetime
from typing import Dict

import portfolio_spec

import click
from prompt_toolkit import prompt
from tabulate import tabulate
from ib_insync import *
from portfolio_spec import *
import doctest
import math
import pandas as pd


@click.group()
def cli():
    pass


def get_net_liquidation_value(ib: IB, account_number: str) -> float:
    for summary in ib.accountSummary():
        if summary.account == account_number and summary.tag == "NetLiquidation":
            return float(summary.value)
    raise Exception("Can't find net liquidation value for %s" % account_number)


def calculate_target_positions(net_liquidation_value: float,
                               prices: pd.Series,
                               weights: Dict[str, float],
                               long_leverage: float = 100) -> Dict[str, int]:
    from pypfopt import DiscreteAllocation
    da = DiscreteAllocation(weights, prices, total_portfolio_value=net_liquidation_value * long_leverage / 100.0)
    alloc, leftover = da.lp_portfolio()
    return alloc


def fetch_ib_contracts(ib: IB, tickers: List[str]) -> Dict[str, Contract]:
    """
    Gets IB contracts for a list of tickers.
    :param ib:
    :param tickers:
    :return:
    """
    out = {}
    for ticker in tickers:
        contracts = ib.reqContractDetails(Stock(ticker, "SMART", "USD"))
        if not contracts:
            raise Exception("Couldn't find IB contract for ticker %s" % ticker)
        if len(contracts) > 1:
            raise Exception("Ambiguous IB contract for ticker %s" % ticker)
        contract = contracts[0].contract
        out[ticker] = contract
    return out


def get_prices_for_contracts(ib: IB, contracts: List[Contract]) -> pd.Series:
    out = {}
    for contract in contracts:
        data = ib.reqMktData(contract)
        while data.last != data.last: ib.sleep(0.01)  # Wait until data is in.
        # print("%s has a last price of %f" % (ticker, data.last))
        out[contract.symbol] = data.last

    return pd.Series(out).sort_index()


def print_rebalance_summary(prices,
                            target_weights: Dict[str, float],
                            target_positions: Dict[str, int],
                            current_positions: Dict[str, int], orders: Dict[str, int]):
    all_tickers = list(set(target_positions.keys()) | set(current_positions.keys()))
    all_tickers.sort()
    data = [
        [ticker, target_weights.get(ticker, ""), current_positions.get(ticker, ""),
         target_positions.get(ticker, ""), orders.get(ticker, ""), prices[ticker], ]
        for ticker in all_tickers]
    print(
        tabulate(data, headers=["Ticker", "Target Weight", "Current Position", "Target Position", "Orders", "Price"]))


def calculate_orders(current_positions: Dict[str, int], target_positions: Dict[str, int], prices: Dict[str, int]) -> \
        Dict[str, int]:
    """
    >>> calculate_orders({"SPY": 1}, {"SPY": 2}, {"SPY": 1000}, 1)
    {'SPY': 1}

    >>> calculate_orders({"SPY": 2}, {"SPY": 1}, {"SPY": 1000}, 1)
    {'SPY': -1}

    >>> calculate_orders({}, {"SPY": 1}, {"SPY": 1000}, 1)
    {'SPY': 1}

    >>> calculate_orders({"SPY": 1}, {}, {"SPY": 1000}, 1)
    {'SPY': -1}

    >>> calculate_orders({"SPY": 1}, {"QQQ": 1}, {"SPY": 1000, "QQQ": 1000}, 1)
    {'QQQ': 1, 'SPY': -1}

    >>> calculate_orders({"SPY": 1}, {"SPY": 2}, {"SPY": 10}, 1000)
    {}

    :param current_positions:
    :param target_positions:
    :param prices: Current ticker prices.
    :return: A map from ticker to shares to buy (positive) or sell (negative).
    """
    out: Dict[str, int] = {}
    all_tickers = sorted(list(set(current_positions.keys()) | set(target_positions.keys())))
    for ticker in all_tickers:
        current = current_positions.get(ticker, 0)
        target = target_positions.get(ticker, 0)
        delta = target - current
        if delta == 0:
            continue
        out[ticker] = delta
    return out


def compute_min_variance_portfolio(tickers: List[str], lookback_history=180) -> Dict[str, float]:
    """
    Compute the min variance portfolio.
    :param tickers:
    :param lookback_history:
    :return: A mapping from the ticker to the weight.
    """
    from pypfopt import expected_returns
    from pypfopt import objective_functions
    from pypfopt import EfficientFrontier
    from pypfopt import risk_models
    from datetime import datetime, timedelta

    import yfinance as yf
    date_N_days_ago = datetime.now() - timedelta(days=lookback_history)
    print("Fetching prices from %s to now" % date_N_days_ago)
    prices = yf.download(tickers, period="max")["Adj Close"][date_N_days_ago:]
    print("Finished fetching prices")
    mu = expected_returns.capm_return(prices)
    S = risk_models.exp_cov(prices, span=120)
    ef = EfficientFrontier(mu, S)
    # if last_weights is not None:
    #     ef.add_objective(objective_functions.transaction_cost, w_prev=pd.Series(last_weights).values, k=0.003)
    ef.add_objective(objective_functions.L2_reg, gamma=.2)  # gamme is the tuning parameter
    ef.min_volatility()
    weights = ef.clean_weights()
    print("Optimized weights", weights)
    ef.portfolio_performance(verbose=True)
    return weights


@click.command()
@click.option('--account_number', prompt='Account number (e.g. Uxxxxxxx)',
              help='Your account number. Starts with a \'U\'')
@click.option('--port', default=4001)
def rebalance(account_number: str, port: int):
    verify_portfolio(portfolio_spec.portfolio)

    target_tickers = set(h.ticker for h in portfolio_spec.portfolio.longs)

    ib = IB()
    ib.connect('127.0.0.1', port, clientId=1)
    ib.reqPositions()
    print("Current Net Liquidation Value %f" % get_net_liquidation_value(ib, account_number))
    current_positions = {p.contract.symbol: p.position for p in ib.positions(account_number)
                         if isinstance(p.contract, Stock)  # Stocks only!
                         }
    print("Retrieved current positions.")
    all_tickers = set(current_positions.keys()) | target_tickers
    all_contracts = fetch_ib_contracts(ib, all_tickers)
    print("Retrieved IB contracts.")
    target_weights = compute_min_variance_portfolio(target_tickers)
    print("Computed min variance portfolio weights.")
    prices = get_prices_for_contracts(ib, all_contracts.values())
    print("Retrieved prices for IB contracts.")
    target_prices = prices.filter(target_weights.keys())
    target_positions = calculate_target_positions(get_net_liquidation_value(ib, account_number),
                                                  target_prices,
                                                  target_weights,
                                                  portfolio_spec.portfolio.long_leverage)
    orders = calculate_orders(current_positions, target_positions, prices)

    print_rebalance_summary(prices, target_weights, target_positions, current_positions, orders)

    if prompt("Submit orders? yes/no").lower() == "yes":
        if ib.reqAllOpenOrders():
            print("WARNING: There are existing live orders!")
        trades = []
        for (ticker, delta) in orders.items():
            action = "BUY" if delta > 0 else "SELL"
            delta = abs(delta)
            ib_order = Order(orderType='MIDPRICE', action=action, totalQuantity=delta)
            trades += [ib.placeOrder(all_contracts[ticker], ib_order)]
            print("%s [%d] shares of [%s]" % (
                ib_order.action, ib_order.totalQuantity, ticker))
            ib.sleep()  # Sleep for a bit to let the TWS order system catch up.
        print("Orders submitted but may take a while to execute. Exiting.")


cli.add_command(rebalance)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rebalance()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
