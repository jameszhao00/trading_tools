from portfolio_types import *

portfolio = Portfolio(leverage=100, holdings=[
    ## Event Driven

    # Covid
    Holding("ABT", 1),

    # Stocks for a really bad hurricane season.
    Holding("HD", 1),
    Holding("LOW", 1),


    ## Brands
    Holding("LULU", 1),
    Holding("AAPL", 1),

    ## Growth

    # Enterprise cloud.
    Holding("CRM", 1),
    Holding("OKTA", 1),
    Holding("AYX", 1),
    Holding("MSFT", 2),
    Holding("TWLO", 1),
    Holding("DOCU", 1),
    Holding("TTD", 1),
    # TODO: Add Snowflake.

    # Devops
    Holding("DDOG", 1),
    Holding("FSLY", 1),

    # Communications.
    Holding("ZM", 1),

    # Payments.
    Holding("SQ", 1),

    # Ecommerce.
    Holding("BABA", 1),
    Holding("ETSY", 1),
    Holding("SHOP", 1),
    Holding("MELI", 2),
    Holding("SE", 1),
    Holding("CVNA", 1),
    Holding("VRM", 1),
    Holding("W", 1),
    Holding("JD", 1),
    Holding("FB", 1),

    # Electronic entertainment.
    Holding("TTWO", 1),
    Holding("EA", 1),
])
