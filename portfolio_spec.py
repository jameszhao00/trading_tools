from portfolio_types import *

portfolio = Portfolio(long_leverage=100, short_leverage=100, holdings=[
    # Longs
    # Growth
    # What to look for:

    # Small/medium Growth.
    Holding("SQ", 10),
    Holding("DDOG", 10),
    Holding("TWLO", 10),
    Holding("SE", 10),
    Holding("ZM", 10),
    Holding("PTON", 1),  # Buy more once it drops a bit.
    Holding("U", 2),  # Game infrastructure. Slowly build up the position.

    Holding("PBW", 10),  # Clean energy.

    # Large cap growth.
    Holding("AMZN", 10),
    Holding("MSFT", 10),
    Holding("AAPL", 10),

    # Shorts
    Holding("QQQ", -70),  # For hedging.
    Holding("XLE", -20),
    Holding("CSCO", -10),  # Things are moving to the cloud. Less need for physical network gear.
    Holding("IBM", -10),  # It's IBM.
    Holding("NKLA", -2),  # Blatant fraud.
    Holding("GSX", -2),  # Some shortable odd chinese edutech compay. https://twitter.com/CitronResearch/status/1260536928606146560
    # Tobacco stocks
    Holding("MO", -2),  # Altria.
    Holding("PM", -2),  # Philip Morris.
])
