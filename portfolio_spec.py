from portfolio_types import *

portfolio = Portfolio(long_leverage=100, short_leverage=70, holdings=[
    # Longs
    #
    Holding("SQ", 10),
    Holding("DDOG", 10),
    Holding("TWLO", 10),
    Holding("SE", 10),
    Holding("ZM", 10),
    Holding("LULU", 10),

    Holding("PBW", 10),  # Clean energy.

    #
    Holding("AMZN", 10),
    Holding("MSFT", 10),
    Holding("AAPL", 10),

    # Shorts
    Holding("QQQ", -80),
    Holding("XLE", -20),
    Holding("CSCO", -10),
    Holding("NKLA", -2),
])
