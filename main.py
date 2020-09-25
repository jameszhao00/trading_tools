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


@click.group()
def cli():
    pass


def get_net_liquidation_value(ib: IB, account_number: str) -> float:
    for summary in ib.accountSummary():
        if summary.account == account_number and summary.tag == "NetLiquidation":
            return float(summary.value)
    raise Exception("Can't find net liquidation value for %s" % account_number)


def calculate_target_positions(net_liquidation_value: float,
                               ticker_prices: Dict[str, float],
                               target_holdings: List[Holding],
                               long_leverage: float = 100,
                               short_leverage: float = 0) -> Dict[str, int]:
    """
    Calculates target positions.

    >>> calculate_target_positions(100, {"SPY", 50}, [Holding("SPY", 0)])
    {}

    >>> calculate_target_positions(10, {"SPY": 1}, [Holding("SPY", 1)])
    {'SPY': 10}

    >>> calculate_target_positions(10, {"SPY": 1}, [Holding("SPY", -1)], short_leverage=100)
    {'SPY': -10}

    >>> calculate_target_positions(10, {"SPY": 1}, [Holding("SPY", 1)], 150)
    {'SPY': 15}

    >>> calculate_target_positions(10, {"SPY": 1}, [Holding("SPY", -1)], short_leverage=150)
    {'SPY': -15}

    >>> calculate_target_positions(10, {"SPY": 6}, [Holding("SPY", 1)])
    {'SPY': 1}

    >>> calculate_target_positions(10, {"SPY": 9}, [Holding("SPY", 1)])
    {'SPY': 1}

    >>> calculate_target_positions(10, {"SPY": 9}, [Holding("SPY", -1)], short_leverage=100)
    {'SPY': -1}

    >>> calculate_target_positions(10, {"SPY": 10}, [Holding("SPY", 1)])
    {'SPY': 1}

    >>> calculate_target_positions(10, {"SPY": 11}, [Holding("SPY", 1)])
    WARNING: Target portfolio contains holding SPY with 0 position
    {}

    >>> calculate_target_positions(10, {"SPY": 11}, [Holding("SPY", -1)], short_leverage=100)
    WARNING: Target portfolio contains holding SPY with 0 position
    {}

    >>> calculate_target_positions(10, {"SPY": 1, "QQQ": 1}, [Holding("SPY", 1), Holding("QQQ", 1)])
    {'SPY': 5, 'QQQ': 5}

    >>> calculate_target_positions(10, {"SPY": 1, "QQQ": 1}, [Holding("SPY", -1), Holding("QQQ", -1)], short_leverage=100)
    {'SPY': -5, 'QQQ': -5}

    >>> calculate_target_positions(10, {"SPY": 1, "QQQ": 1}, [Holding("SPY", 1), Holding("QQQ", 2)])
    {'SPY': 3, 'QQQ': 6}

    >>> calculate_target_positions(10, {"SPY": 1, "QQQ": 1}, [Holding("SPY", -1), Holding("QQQ", -2)], short_leverage=100)
    {'SPY': -3, 'QQQ': -6}

    >>> calculate_target_positions(10, {"SPY": 1, "QQQ": 1}, [Holding("SPY", 1), Holding("QQQ", 3)])
    {'SPY': 2, 'QQQ': 7}

    >>> calculate_target_positions(10, {"SPY": 1, "QQQ": 3}, [Holding("SPY", 1), Holding("QQQ", 3)])
    {'SPY': 2, 'QQQ': 2}

    >>> calculate_target_positions(10, {"SPY": 1, "QQQ": 7}, [Holding("SPY", 1), Holding("QQQ", 3)])
    {'SPY': 2, 'QQQ': 1}

    >>> calculate_target_positions(10, {"SPY": 1, "QQQ": 8}, [Holding("SPY", 1), Holding("QQQ", 3)])
    WARNING: Target portfolio contains holding QQQ with 0 position
    {'SPY': 2}

    >>> calculate_target_positions(10, {"SPY": 1, "QQQ": 10}, [Holding("SPY", 1), Holding("QQQ", 3)])
    WARNING: Target portfolio contains holding QQQ with 0 position
    {'SPY': 2}

    >>> calculate_target_positions(10, {"SPY": 1, "QQQ": 1}, [Holding("SPY", -1), Holding("QQQ", 1)], \
        long_leverage=100, short_leverage=50)
    {'SPY': -5, 'QQQ': 10}
    """
    total_long_weight = sum([h.weight for h in target_holdings if h.weight > 0])
    # total_short_weight is a negative value.
    total_short_weight = sum([h.weight for h in target_holdings if h.weight < 0])

    if total_long_weight < 0:
        raise Exception("Total long weight must be 0 or more!")
    if total_short_weight > 0:
        raise Exception("Total short short weight must be 0 or less!")
    out = {}
    for holding in target_holdings:
        if holding.weight == 0:
            continue
        target_percent = holding.weight / (
            float(total_long_weight) if holding.weight > 0 else float(-total_short_weight))
        price = ticker_prices[holding.ticker]
        if price <= 0:
            raise Exception("Ticker %s has a invalid price: " % (holding.ticker, price))
        leverage = long_leverage if holding.weight > 0 else short_leverage
        target_position = (target_percent * (net_liquidation_value * leverage / 100.0) / price)
        if holding.weight > 0:
            target_position = math.floor(target_position)
        else:
            target_position = math.ceil(target_position)
        if target_position == 0:
            print("WARNING: Target portfolio contains holding %s with 0 position" % holding.ticker)
        else:
            out[holding.ticker] = target_position
    return out


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


def get_prices_for_contracts(ib: IB, contracts: List[Contract]) -> Dict[str, float]:
    out = {}
    for contract in contracts:
        data = ib.reqMktData(contract)
        while data.last != data.last: ib.sleep(0.01)  # Wait until data is in.
        # print("%s has a last price of %f" % (ticker, data.last))
        out[contract.symbol] = data.last
    return out


def print_rebalance_summary(target_holdings: List[Holding], prices, target_positions: Dict[str, int],
                            current_positions: Dict[str, int], orders: Dict[str, int]):
    all_tickers = set(target_positions.keys()) | set(current_positions.keys())
    target_holdings = {h.ticker: h.weight for h in target_holdings}
    data = [
        [ticker, prices[ticker], current_positions.get(ticker, ""), target_holdings.get(ticker, ""),
         target_positions.get(ticker, ""), orders.get(ticker, "")]
        for ticker in all_tickers]
    print(tabulate(data, headers=["Ticker", "Price", "Current Position", "Target Weight", "Target Position", "Orders"]))


def calculate_orders(current_positions: Dict[str, int], target_positions: Dict[str, int]) -> Dict[str, int]:
    """
    >>> calculate_orders({"SPY": 1}, {"SPY": 2})
    {'SPY': 1}

    >>> calculate_orders({"SPY": 2}, {"SPY": 1})
    {'SPY': -1}

    >>> calculate_orders({}, {"SPY": 1})
    {'SPY': 1}

    >>> calculate_orders({"SPY": 1}, {})
    {'SPY': -1}

    >>> calculate_orders({"SPY": 1}, {"QQQ": 1})
    {'QQQ': 1, 'SPY': -1}

    :param current_positions:
    :param target_positions:
    :return: A map from ticker to shares to buy (positive) or sell (negative).
    """
    out: Dict[str, int] = {}
    all_tickers = sorted(list(set(current_positions.keys()) | set(target_positions.keys())))
    for ticker in all_tickers:
        current = current_positions.get(ticker, 0)
        target = target_positions.get(ticker, 0)
        delta = target - current
        if delta != 0:
            out[ticker] = delta
    return out


@click.command()
@click.option('--account_number', prompt='Account number (e.g. Uxxxxxxx)',
              help='Your account number. Starts with a \'U\'')
@click.option('--port', default=7496)
def rebalance(account_number: str, port: int):
    verify_portfolio(portfolio_spec.portfolio)

    target_holdings = portfolio_spec.portfolio.holdings
    target_tickers = set(h.ticker for h in portfolio_spec.portfolio.holdings)

    ib = IB()
    ib.connect('127.0.0.1', port, clientId=1)
    ib.reqPositions()
    print("Current Net Liquidation Value %f" % get_net_liquidation_value(ib, account_number))
    current_positions = {p.contract.symbol: p.position for p in ib.positions(account_number)
                         if isinstance(p.contract, Stock)  # Stocks only!
                         }
    all_tickers = set(current_positions.keys()) | target_tickers
    all_contracts = fetch_ib_contracts(ib, all_tickers)
    prices = get_prices_for_contracts(ib, all_contracts.values())
    tgt_positions = calculate_target_positions(get_net_liquidation_value(ib, account_number), prices, target_holdings,
                                               portfolio_spec.portfolio.long_leverage,
                                               portfolio_spec.portfolio.short_leverage)
    orders = calculate_orders(current_positions, tgt_positions)
    print_rebalance_summary(target_holdings, prices, tgt_positions, current_positions, orders)

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
