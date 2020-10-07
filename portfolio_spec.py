from portfolio_types import *

# Major themes:
# Stimulus delayed.

portfolio = Portfolio(long_leverage=130, short_leverage=60, holdings=[
    # Longs

    # Growth
    # What to look for:
    # Small/medium Growth.
    Holding("SQ", 8, reason="Leader in ECommerce payment solutions.", founder_lead=True, glassdoor_ceo_rating=87),
    Holding("DDOG", 10, reason="Leader in production monitoring", founder_lead=True, glassdoor_ceo_rating=93),
    Holding("TWLO", 10, reason="Leader in communication IaaS and call centers", founder_lead=True,
            glassdoor_ceo_rating=92, hiring_surge=True),
    Holding("SE", 10, reason="Leader in Ecommerce in SE Asia", founder_lead=True, glassdoor_ceo_rating=67),
    Holding("NVDA", 10, reason="Leader in Machine learning", founder_lead=True, glassdoor_ceo_rating=99),

    Holding("ZG", 5, reason="Leader in Home purchasing", founder_lead=True, glassdoor_ceo_rating=93),
    # Holding("RDFN", 1, reason="Leader in Home purchasing", founder_lead=True, glassdoor_ceo_rating=74),

    # Remote Productivity Leaders.
    Holding("TEAM", 5, reason="Leader in project management. There's strong network effects in project management. If "
                              "I'm used to JIRA I really don't want to switch to Asana.", founder_lead=True,
            glassdoor_ceo_rating=97),
    Holding("ZM", 5, reason="Leader in communication. Somewhat strong network effects.", founder_lead=True,
            glassdoor_ceo_rating=98),
    Holding("PTON", 5, reason="Leader in home fitness", tactical="Buy more once it drops a bit.", founder_lead=True,
            glassdoor_ceo_rating=91),

    Holding("U", 3, reason="Leader in game/interactive experiences IaaS.", tactical="Slowly build up the position.",
            glassdoor_ceo_rating=92),
    Holding("SNOW", 3, reason="Best product at data warehousing/analytics.", tactical="Slowly build up the position.",
            founder_lead=True, glassdoor_ceo_rating=89),

    # ECommerce.
    # Why not Carvana? Because the CEO is a convicted felon.
    Holding("W", 1, reason="Online furniture company.", tactical="Slowly build up a position.", founder_lead=True,
            glassdoor_ceo_rating=57),
    Holding("ETSY", 4, reason="Leader in quirky online shopping. Different than amazon. Great moat.",
            glassdoor_ceo_rating=82),

    Holding("HUBS", 3, reason="Amazing Glassdoor reviews.", tactical="Slowly build up a position?", founder_lead=True,
            glassdoor_ceo_rating=98),
    Holding("DOCU", 3, reason="Leader in document management.", tactical="Slowly build up a position?",
            founder_lead=True, glassdoor_ceo_rating=98),
    Holding("TTD", 3, reason="???", tactical="Slowly build up a position?", founder_lead=True, glassdoor_ceo_rating=87),
    Holding("ROKU", 5, reason="Leader in home entertainment", founder_lead=True, glassdoor_ceo_rating=78,
            hiring_surge=True),
    Holding("ZS", 3, reason="Security. Massive hiring surge."),
    Holding("FIVN", 5, reason="Leader in contact center tech."),

    Holding("PBW", 13, reason="Clean energy"),
    Holding("ICLN", 7, reason="Clean energy"),

    # Shorts.
    # Tech.
    Holding("CSCO", -3, reason="Things are moving to the cloud. Less need for physical network gear."),
    Holding("INTC", -3, reason="Less desktops. Server chips are moving to ARM/in house processors/GPUs."),
    Holding("DBX", -3, reason="Google/Microsoft/... cloud storage owning this.", founder_lead=True),
    Holding("BOX", -3, reason="Google/Microsoft/... cloud storage owning this.", founder_lead=True),
    Holding("NLOK", -3,
            reason="Newer devices do not need consumer facing antivirus. How many people buy consumer fraud prevention?"),
    Holding("CLDR", -3, reason="Cloudera's been left behind by companies like Snowflake."),
    Holding("IBM", -3, reason="It's IBM"),
    Holding("VRSN", -3, reason="Verisign is massively rent seeking. Doesn't innovate."),

    # Energy and finance.
    Holding("XLE", -11),
    Holding("XLF", -7),
    # Tobacco stocks
    Holding("MO", -3, reason="Smoking on the decline"),
    Holding("PM", -3, reason="Smoking on the decline"),
])
