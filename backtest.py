# universe
from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd
import plotly.express as px
import pandas as pd

from stock_data_repo import StockDataRepo

# Download some additional days of data so we guarantee enough days of lookback.
ADDITIONAL_LOOKBACK_BUFFER = 10


@dataclass
class BacktestResult:
    allocation_history: pd.DataFrame
    returns_history: pd.Series
    aux_data_history: pd.Series
    component_returns: pd.DataFrame


class Backtester:
    def __init__(self, start_date: datetime, end_date=None, max_lookback_in_days: int = 120):
        self.max_lookback_in_days = max_lookback_in_days
        self.start_date = start_date
        self.repo = StockDataRepo(start_date - timedelta(days=max_lookback_in_days + ADDITIONAL_LOOKBACK_BUFFER),
                                  end_date)

    def backtest(self, long_universe: List[str], short_universe: List[str], portfolio_fn) -> BacktestResult:
        universe = long_universe + short_universe
        universe.sort()
        component_returns = self.repo.get_prices(universe).pct_change()[1:]
        for short_ticker in short_universe:
            component_returns["SHORT_" + short_ticker] = -1 * component_returns[short_ticker]
            del component_returns[short_ticker]

        result_datetime_index = component_returns.index[component_returns.index >= self.start_date]
        allocation_history = pd.DataFrame(index=result_datetime_index, columns=component_returns.columns, dtype=np.float)
        returns_history = pd.Series(index=result_datetime_index, dtype=np.float)
        aux_data_history = pd.Series(index=result_datetime_index, dtype=object)
        last_allocation = {ticker: 0 for ticker in universe}

        for current_date in result_datetime_index:
            # Compute the NAV using yesterday's allocation history.
            returns_history.loc[current_date] = (component_returns.loc[current_date] * pd.Series(last_allocation)).sum()

            # Then compute and store today's allocation.
            # Get the data from 11 days in the past to 1 day in the past.
            returns_excluding_today = component_returns.loc[:current_date].iloc[-self.max_lookback_in_days - 1:-1]
            # Drop any tickers with any missing data.
            returns_excluding_today = returns_excluding_today.dropna(axis=1)
            last_allocation, aux_data = portfolio_fn(current_date, returns_excluding_today)

            # Add back tickers with missing data.
            for ticker in universe:
                if ticker not in last_allocation:
                    last_allocation[ticker] = 0

            aux_data_history[current_date] = aux_data
            allocation_history.loc[current_date] = last_allocation
        return BacktestResult(allocation_history=allocation_history, returns_history=returns_history,
                              aux_data_history=aux_data_history, component_returns=component_returns)
