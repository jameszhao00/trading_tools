from portfolio_types import *

# Major themes:
# Stimulus delayed.

portfolio = Portfolio(long_leverage=100, short_leverage=0, holdings=[
    # Longs

    # Growth
    # What to look for:
    # Small/medium Growth.
    Holding("SQ", 8, reason="Leader in ECommerce payment solutions.", is_founder_active=True, glassdoor_ceo_rating=87),
    Holding("DDOG", 10, reason="Leader in production monitoring", is_founder_active=True, glassdoor_ceo_rating=93),
    Holding("TWLO", 10, reason="Leader in communication IaaS and call centers", is_founder_active=True,
            glassdoor_ceo_rating=92, hiring_surge=True),
    Holding("SE", 10, reason="Leader in Ecommerce in SE Asia", is_founder_active=True, glassdoor_ceo_rating=67),
    Holding("NVDA", 10, reason="Leader in Machine learning", is_founder_active=True, glassdoor_ceo_rating=99),
    Holding("FSLY", 10, reason="Leader in CDNs", is_founder_active=True, glassdoor_ceo_rating=100),

    Holding("ZM", 4, reason="Leader in communication. Somewhat strong network effects.", is_founder_active=True,
            glassdoor_ceo_rating=98),
    Holding("PTON", 5, reason="Leader in home fitness", tactical="Buy more once it drops a bit.", is_founder_active=True,
            glassdoor_ceo_rating=91),
    Holding("ETSY", 4, reason="Leader in quirky online shopping. Different than amazon. Great moat.",
            glassdoor_ceo_rating=82),
    Holding("DOCU", 4, reason="Leader in document management.", tactical="Slowly build up a position?",
            is_founder_active=True, glassdoor_ceo_rating=98),
    Holding("TTD", 4, reason="???", tactical="Slowly build up a position?", is_founder_active=True, glassdoor_ceo_rating=87),
    Holding("ROKU", 5, reason="Leader in home entertainment", is_founder_active=True, glassdoor_ceo_rating=78,
            hiring_surge=True),
    Holding("ZS", 3, reason="Security. Massive hiring surge."),
    Holding("FIVN", 5, reason="Leader in contact center tech."),

    Holding("PBW", 10, reason="Clean energy"),
    Holding("ICLN", 5, reason="Clean energy"),

    Holding("AAPL", 8, reason="Leader in consumer tech."),
    Holding("AMZN", 8, reason="Leader in general innovation and ecommerce"),

    # Zillow CEO seems really MBA.
    # Holding("ZG", 5, reason="Leader in Home purchasing", is_founder_active=True, glassdoor_ceo_rating=93),
    # Holding("RDFN", 1, reason="Leader in Home purchasing", is_founder_active=True, glassdoor_ceo_rating=74),
    # Holding("SNAP", 3, reason="Leader in teen social media", is_founder_active=True, glassdoor_ceo_rating=77),
    # Per glassdoor snap's culture is apparently really douchey.

    # Remote Productivity Leaders.
    # Holding("TEAM", 5, reason="Leader in project management. There's strong network effects in project management. If "
    #                           "I'm used to JIRA I really don't want to switch to Asana.", is_founder_active=True,
    #         glassdoor_ceo_rating=97),
    # Holding("SHOP", 3, reason="Amazing Glassdoor reviews.", tactical="Slowly build up a position?"),

    # Holding("HUBS", 3, reason="Amazing Glassdoor reviews.", tactical="Slowly build up a position?", is_founder_active=True,
    #         glassdoor_ceo_rating=98),
    #
    # Holding("U", 3, reason="Leader in game/interactive experiences IaaS.", tactical="Slowly build up the position.",
    #         glassdoor_ceo_rating=92),
    # Holding("SNOW", 3, reason="Best product at data warehousing/analytics.", tactical="Slowly build up the position.",
    #         is_founder_active=True, glassdoor_ceo_rating=89),

    # ECommerce.
    # Why not Carvana? Because the CEO is a convicted felon.
    # Holding("W", 1, reason="Online furniture company.", tactical="Slowly build up a position.", is_founder_active=True,
    #         glassdoor_ceo_rating=57),
    # Shorts.
    # Tech.
    # Holding("CSCO", -3, reason="Things are moving to the cloud. Less need for physical network gear."),
    # Holding("INTC", -3, reason="Less desktops. Server chips are moving to ARM/in house processors/GPUs."),
    # Holding("DBX", -3, reason="Google/Microsoft/... cloud storage owning this.", is_founder_active=True),
    # Holding("BOX", -3, reason="Google/Microsoft/... cloud storage owning this.", is_founder_active=True),
    # Holding("NLOK", -3,
    #         reason="Newer devices do not need consumer facing antivirus. How many people buy consumer fraud prevention?"),
    # Holding("CLDR", -3, reason="Cloudera's been left behind by companies like Snowflake."),
    # Holding("IBM", -3, reason="It's IBM"),
    # Holding("VRSN", -3, reason="Verisign is massively rent seeking. Doesn't innovate."),
    #
    # # Energy and finance.
    # Holding("XLE", -11),
    # Holding("XLF", -7),
    # # Tobacco stocks
    # Holding("MO", -3, reason="Smoking on the decline"),
    # Holding("PM", -3, reason="Smoking on the decline"),
])
