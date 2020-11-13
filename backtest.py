# universe
import os
from dataclasses import dataclass
from typing import Dict, List
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd
import plotly.express as px
import pandas as pd
from datetime import datetime
from stock_data_repo import StockDataRepo
from fbprophet import Prophet

# Download some additional days of data so we guarantee enough days of lookback.
ADDITIONAL_LOOKBACK_BUFFER = 10


@dataclass
class BacktestResult:
    allocation_history: pd.DataFrame
    returns_history: pd.Series
    aux_data_history: pd.Series
    component_returns: pd.DataFrame

    def save_most_recent_allocation(self, directory: str, leverage=1.0):
        path = os.path.join(directory, datetime.now().strftime("optimized-allocation-%Y-%m-%d__%H-%M-%S") + ".csv")
        allocation = self.allocation_history.iloc[-1] * leverage
        allocation = allocation[allocation != 0]
        allocation.rename("weight").to_csv(path, index_label=["ticker"])
        return path


class Backtester:
    def __init__(self, start_date: datetime, end_date=None, max_lookback_in_days: int = 120,
                 start_when_all_data_is_available=False):
        self.max_lookback_in_days = max_lookback_in_days
        self.start_date = start_date
        self.end_date = end_date
        self.repo = StockDataRepo(start_date - timedelta(days=max_lookback_in_days + ADDITIONAL_LOOKBACK_BUFFER),
                                  end_date)
        # Whether to start backtesting when all tickers have all data available. Default is to start the backtest when
        # any tickers have data.
        self.start_when_all_data_is_available = start_when_all_data_is_available

    def backtest(self, long_universe: List[str], short_universe: List[str], portfolio_fn) -> BacktestResult:
        universe = long_universe + short_universe
        universe.sort()
        assert len(universe) == len(set(universe)), "Universe should be unique!"
        component_returns = self.repo.get_prices(universe).pct_change()[1:]
        # Move the start date back if we're missing data.
        earliest_possible_start_date = component_returns.index[0] + timedelta(days=self.max_lookback_in_days)
        corrected_start_date = (
            earliest_possible_start_date if earliest_possible_start_date > self.start_date else self.start_date)

        result_datetime_index = component_returns.index[component_returns.index >= corrected_start_date]

        allocation_history = pd.DataFrame(index=result_datetime_index, columns=universe,
                                          dtype=np.float)
        returns_history = pd.Series(index=result_datetime_index, dtype=np.float)
        aux_data_history = pd.Series(index=result_datetime_index, dtype=object)
        last_allocation = {ticker: 0 for ticker in universe}

        for current_date in result_datetime_index:

            # Compute the NAV using yesterday's allocation history.
            returns_history.loc[current_date] = (component_returns.loc[current_date] * pd.Series(last_allocation)).sum()

            # Then compute and store today's allocation.
            # Get the data from 11 days in the past to 1 day in the past.
            returns_excluding_today = component_returns.loc[:current_date].iloc[-self.max_lookback_in_days - 1:-1]
            if self.start_when_all_data_is_available:
                if returns_excluding_today.isnull().values.any():
                    continue
            else:
                # Drop any tickers with any missing data.
                returns_excluding_today = returns_excluding_today.dropna(axis=1)
            # Transparently treat the shorts as longs by inverting their returns.
            for short_ticker in short_universe:
                returns_excluding_today["SHORT_" + short_ticker] = -1 * returns_excluding_today[short_ticker]
                # Maybe this is also in the long universe.
                if short_ticker not in long_universe:
                    del returns_excluding_today[short_ticker]

            last_allocation, aux_data = portfolio_fn(current_date, returns_excluding_today)
            last_allocation = pd.Series(last_allocation)

            # Fix the short names and flip their weights.
            def maybe_flip_short_name(ticker: str):
                if ticker.startswith("SHORT_"):
                    return ticker.replace("SHORT_", "")
                return ticker

            def maybe_flip_short_weight(ticker: str, weight: float):
                if ticker.startswith("SHORT_"):
                    return -1 * weight
                return weight

            last_allocation = pd.Series({
                maybe_flip_short_name(ticker): maybe_flip_short_weight(ticker, weight)
                for ticker, weight in last_allocation.iteritems()
            })
            # Assert that if a ticker is in both the long universe and the short universe it only has one weight.
            assert last_allocation.index.is_unique

            # Normalize it so longs sum up to 100% weight.
            total_long_weight = last_allocation[last_allocation > 0].sum()
            last_allocation = last_allocation.map(lambda w: w / total_long_weight)

            # Add back tickers with missing data.
            for ticker in universe:
                if ticker not in last_allocation:
                    last_allocation[ticker] = 0

            aux_data_history[current_date] = aux_data
            allocation_history.loc[current_date] = last_allocation
        return BacktestResult(allocation_history=allocation_history, returns_history=returns_history,
                              aux_data_history=aux_data_history, component_returns=component_returns)


@dataclass
class ForecastResults:
    predictions: pd.Series
    lower_confidence_interval: pd.Series
    upper_confidence_interval: pd.Series
    raw_forecast: pd.DataFrame
    prophet_instance: Prophet


def forecast(series: pd.Series, forecast_window=30, confidence_interval=.95) -> ForecastResults:
    df = pd.DataFrame({
        "y": series.values,
        "ds": series.index
    })
    m = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False,
                interval_width=confidence_interval)
    m.fit(df)
    future = m.make_future_dataframe(periods=forecast_window)
    forecast: pd.DataFrame = m.predict(future)
    # Slice just the future and set the axis.
    postprocessed_forecast = forecast.set_index("ds").rename_axis("Date")[series.index[-1]:].iloc[1:]
    return ForecastResults(predictions=postprocessed_forecast["yhat"],
                           lower_confidence_interval=postprocessed_forecast["yhat_lower"],
                           upper_confidence_interval=postprocessed_forecast["yhat_upper"],
                           raw_forecast=forecast,
                           prophet_instance=m)
