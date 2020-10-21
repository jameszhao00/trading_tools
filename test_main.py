from unittest import TestCase
from main import calculate_target_positions

import pandas as pd


class Test(TestCase):

    def test_calculate_target_positions(self):
        r = calculate_target_positions(1000,
                                       prices=pd.Series({"AAPL": 10, "GOOG": 20, "QQQ": 50, "SPY": 100, "MSFT": 200}),
                                       weights={
                                           "AAPL": 1.0,
                                           "GOOG": 2.0,
                                           "MSFT": 3.0,
                                           "QQQ": -2.0,
                                           "SPY": -1.0,
                                       })
        self.assertDictEqual(r, {"AAPL": 1 * 1000 / 10, "GOOG": 2 * 1000 / 20, "MSFT": 3.0 * 1000 / 200,
                                 "QQQ": -2.0 * 1000 / 50, "SPY": -1.0 * 1000 / 100})
