from datetime import datetime
from typing import Dict, Tuple
from unittest import TestCase

from pandas import DatetimeIndex
from pandas._testing import assert_frame_equal, assert_series_equal
import pandas as pd
import tempfile
from backtest import Backtester, forecast


def noop_set_portfolio(timestamp, returns_excluding_today) -> Tuple[Dict[str, float], object]:
    assert timestamp not in returns_excluding_today
    return {"AAPL": 1, "GOOG": 0}, 1


class TestBacktester(TestCase):
    def test_backtest(self):
        sut = Backtester(start_date=datetime(2020, 3, 5), end_date=datetime(2020, 3, 10), max_lookback_in_days=1)
        r = sut.backtest(["AAPL", "GOOG"], [], noop_set_portfolio)
        assert_series_equal(r.returns_history,
                            pd.Series(index=DatetimeIndex(['2020-03-05', '2020-03-06', '2020-03-09'], name='Date'),
                                      data=[0.0, -0.013280012625504156, -0.07909216101874683]))
        assert_frame_equal(r.allocation_history,
                           pd.DataFrame(index=DatetimeIndex(['2020-03-05', '2020-03-06', '2020-03-09'], name='Date'),
                                        data={"AAPL": [1.0, 1.0, 1.0], "GOOG": [0.0, 0.0, 0.0]}))

        assert_frame_equal(r.component_returns,
                           pd.DataFrame(index=DatetimeIndex(
                               ["2020-02-25", "2020-02-26", "2020-02-27", "2020-02-28", "2020-03-02", "2020-03-03",
                                "2020-03-04", "2020-03-05", "2020-03-06", "2020-03-09"], name='Date'),
                               data={"AAPL": [-0.033872, 0.015864, -0.065368, -0.000585, 0.093101, -0.031759, 0.046385,
                                              -0.032437, -0.013280, -0.079092],
                                     "GOOG": [-0.023312, 0.003407, -0.053898, 0.016114, 0.037168, -0.034353, 0.033644,
                                              -0.048669, -0.015640, -0.063809]}), check_exact=False,
                           check_less_precise=True)

        assert_series_equal(r.aux_data_history, pd.Series(data=[1, 1, 1],
                                                          index=DatetimeIndex(
                                                              ['2020-03-05', '2020-03-06', '2020-03-09'], name='Date'),
                                                          dtype=object))


class TestBacktestResult(TestCase):
    def test_save_most_recent_allocation(self):
        with tempfile.TemporaryDirectory() as directory:
            sut = Backtester(start_date=datetime(2020, 3, 5), end_date=datetime(2020, 3, 10),
                             max_lookback_in_days=1).backtest(
                ["AAPL", "GOOG"], [], noop_set_portfolio)
            file = sut.save_most_recent_allocation(directory)
            assert file.endswith(".csv")
            assert_frame_equal(pd.read_csv(file), pd.DataFrame({"ticker": ["AAPL", "GOOG"], "weight": [1.0, 0.0]}))

    def test_save_most_recent_allocation_with_leverage(self):
        with tempfile.TemporaryDirectory() as directory:
            sut = Backtester(start_date=datetime(2020, 3, 5), end_date=datetime(2020, 3, 10),
                             max_lookback_in_days=1).backtest(
                ["AAPL", "GOOG"], [], noop_set_portfolio)
            file = sut.save_most_recent_allocation(directory, leverage=2)
            assert_frame_equal(pd.read_csv(file), pd.DataFrame({"ticker": ["AAPL", "GOOG"], "weight": [2.0, 0.0]}))


class Test(TestCase):
    def test_forecast(self):
        s = pd.Series(index=pd.date_range(start='1/1/2018', periods=5, freq='1D'), data=[1, 2, 3, 4, 5])
        results = forecast(s, forecast_window=5)
        assert_series_equal(results.predictions,
                            pd.Series(index=pd.date_range(start='1/6/2018', periods=5, freq='1D').values,
                                      data=[6.0, 7.0, 8.0, 9.0, 10.0]).rename_axis("Date").rename("yhat"))
        assert_series_equal(results.lower_confidence_interval,
                            pd.Series(index=pd.date_range(start='1/6/2018', periods=5, freq='1D').values,
                                      data=[6.0, 7.0, 8.0, 9.0, 10.0]).rename_axis("Date").rename("yhat_lower"))
        assert_series_equal(results.upper_confidence_interval,
                            pd.Series(index=pd.date_range(start='1/6/2018', periods=5, freq='1D').values,
                                      data=[6.0, 7.0, 8.0, 9.0, 10.0]).rename_axis("Date").rename("yhat_upper"))
