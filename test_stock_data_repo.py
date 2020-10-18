from datetime import datetime
from unittest import TestCase

from pandas import DatetimeIndex
from pandas._testing import assert_frame_equal

import pandas as pd

from stock_data_repo import StockDataRepo


class TestStockDataRepo(TestCase):
    def test_get_returns(self):
        repo = StockDataRepo(datetime(2020, 10, 1, 0, 0, 0), datetime(2020, 10, 4, 0, 0, 0))
        repo.get_prices(["AAPL"])
        assert_frame_equal(repo.get_prices(["AAPL", "QQQ"]), pd.DataFrame(
            data={"AAPL": [116.79000091552734, 113.0199966430664], "QQQ": [282.25, 274.30999755859375]},
            index=DatetimeIndex(
                ['2020-10-01', '2020-10-02'], name="Date")))
