from datetime import datetime
from typing import List

import pandas as pd
import yfinance as yf


class StockDataRepo:
    def __init__(self, start_date: datetime, end_date: datetime = None):
        self.start_date = start_date
        self.end_date = end_date
        self.data = None

    def get_prices(self, tickers: List[str]):
        to_fetch = []
        if self.data is None:
            to_fetch = tickers
        else:
            for ticker in tickers:
                if ticker not in self.data:
                    to_fetch.append(ticker)

        if to_fetch:
            prices = yf.download(to_fetch, self.start_date, self.end_date)["Adj Close"]
            if len(to_fetch) == 1:
                # Correct the column name because it's currently Adj Close.
                prices = pd.DataFrame({to_fetch[0]: prices})
            if self.data is not None:
                self.data = pd.concat([self.data, prices], axis=1)
            else:
                self.data = prices
        return self.data[tickers]
