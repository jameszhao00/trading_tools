from typing import Dict, Optional, Tuple, List

import click
from prompt_toolkit import prompt
from tabulate import tabulate
from ib_insync import *
import pandas as pd
import numpy as np

from os import listdir
from os.path import isfile, join


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
                               weights: Dict[str, float]) -> Dict[str, int]:
    # Do the longs and shorts separately, because the DiscreteAllocation can't handle longs and shorts at the same time
    # in a way we want.

    weights_series = pd.Series(weights)
    long_weights = weights_series[weights_series > 0]
    short_weights = weights_series[weights_series < 0]

    # Flip the short weights to be positive.
    short_weights = -short_weights

    total_long_weights = long_weights.sum()
    total_short_weights = short_weights.sum()
    assert total_long_weights > 0  # Could vary due to leverage.

    target_long_value = total_long_weights * net_liquidation_value

    # Finally, normalize the weights so that it sums up to 1.
    long_weights = long_weights / total_long_weights

    long_prices = prices.loc[long_weights.keys()]

    def calc_positions(prices, weights, portfolio_value):
        from pypfopt import DiscreteAllocation
        da = DiscreteAllocation(weights, prices, total_portfolio_value=portfolio_value)
        alloc, leftover = da.greedy_portfolio()
        return alloc

    long_positions = calc_positions(long_prices, long_weights.to_dict(), target_long_value)
    positions = long_positions
    if total_short_weights > 0:
        target_short_value = total_short_weights * net_liquidation_value
        short_weights = short_weights / total_short_weights
        short_prices = prices.loc[short_weights.keys()]
        short_positions = calc_positions(short_prices, short_weights.to_dict(), target_short_value)
        # Flip the short positions to be negative.
        short_positions = {ticker: -position for ticker, position in short_positions.items()}
        for (ticker, weight) in short_positions.items():
            positions[ticker] = weight
    return positions


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


def get_most_recent_allocation(directory: str) -> Tuple[Optional[str], Optional[pd.DataFrame]]:
    """
    Get the most recent allocation.
    :param directory:
    :return: If exists, the allocation file name and the loaded dataframe.
    """
    files = [f for f in listdir(directory) if isfile(join(directory, f))]
    files.sort(reverse=True)
    if files:
        file = files[0]
        df = pd.read_csv(join(directory, file), index_col="ticker")
        return file, df
    return None, None


@click.command()
@click.option('--account_number', prompt='Account number (e.g. Uxxxxxxx)',
              help='Your account number. Starts with a \'U\'')
@click.option('--allocations_directory', prompt='Allocations directory', default="./allocations")
@click.option('--port', default=4001)
def rebalance(account_number: str, allocations_directory: str, port: int):
    file, allocation = get_most_recent_allocation(allocations_directory)
    if not file:
        print("No allocation file found!")
        return

    if prompt("Use allocation file {}? yes/no".format(file)).lower() != "yes":
        return
    allocation = allocation[allocation["weight"] != 0]
    allocation: Dict[str, float] = allocation.to_dict()["weight"]

    print("allocation", allocation)
    target_tickers = set(allocation.keys())

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
    prices = get_prices_for_contracts(ib, all_contracts.values())
    print("Retrieved prices for IB contracts.")
    target_prices = prices.filter(target_tickers)
    target_positions = calculate_target_positions(get_net_liquidation_value(ib, account_number),
                                                  target_prices,
                                                  allocation)
    orders = calculate_orders(current_positions, target_positions, prices)

    print_rebalance_summary(prices, allocation, target_positions, current_positions, orders)

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
