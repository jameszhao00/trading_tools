from dataclasses import dataclass
from typing import List

import collections


@dataclass()
class Holding:
    ticker: str
    weight: int
    reason: str = '[No Reason]'
    tactical: str = ''  # Short term notes.
    is_founder_active: bool = False  # Is the founder active in the company?
    glassdoor_ceo_rating: int = None
    hiring_surge: bool = False


@dataclass()
class Portfolio:
    # Leverage in percent (e.g. 130 = 1.3x leverage).
    long_leverage: float
    holdings: List[Holding]
    short_leverage: float = 0


def verify_portfolio(p: Portfolio):
    """
    >>> verify_portfolio(Portfolio(long_leverage=1, holdings=[Holding("SPY", 1), Holding("SPY", 1)]))
    Traceback (most recent call last):
      ...
    Exception: Found duplicate tickers: ['SPY']

    >>> verify_portfolio(Portfolio(long_leverage=1, holdings=[Holding("SPY", 0)]))
    Traceback (most recent call last):
      ...
    Exception: Found holdings with zero weight: [Holding(ticker='SPY', weight=0)]
    """
    duplicate_items = [item for item, count in collections.Counter([h.ticker for h in p.holdings]).items() if count > 1]
    if duplicate_items:
        raise Exception("Found duplicate tickers: %s" % duplicate_items)

    holding_with_zero_weight = [h for h in p.holdings if h.weight == 0]
    if holding_with_zero_weight:
        raise Exception("Found holdings with zero weight: %s" % holding_with_zero_weight)
