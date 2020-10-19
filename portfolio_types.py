from dataclasses import dataclass
from typing import List

import collections


@dataclass()
class Holding:
    ticker: str
    reason: str = '[No Reason]'
    tactical: str = ''  # Short term notes.
    is_founder_active: bool = False  # Is the founder active in the company?
    glassdoor_ceo_rating: int = None
    hiring_surge: bool = False


@dataclass()
class Portfolio:
    # Leverage in percent (e.g. 130 = 1.3x leverage).
    long_leverage: float
    longs: List[Holding]
    shorts: List[Holding]
    short_leverage: float = 0


def verify_portfolio(p: Portfolio):
    """
    >>> verify_portfolio(Portfolio(long_leverage=1, holdings=[Holding("SPY", 1), Holding("SPY", 1)]))
    Traceback (most recent call last):
      ...
    Exception: Found duplicate tickers: ['SPY']
    """
    duplicate_items = [item for item, count in collections.Counter([h.ticker for h in p.longs]).items() if count > 1]
    if duplicate_items:
        raise Exception("Found duplicate tickers: %s" % duplicate_items)
