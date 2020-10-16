from portfolio_types import *

# Major themes:
# Stimulus delayed.

portfolio = Portfolio(long_leverage=100, short_leverage=60, holdings=[
    # Sector growth.
    Holding("PBW", 20, reason="Clean energy"),

    # High Conviction.
    Holding("DDOG", 10, reason="Leader in production monitoring", is_founder_active=True, glassdoor_ceo_rating=93,
            hiring_surge=True),
    Holding("TWLO", 10, reason="Leader in communication IaaS and call centers", is_founder_active=True,
            glassdoor_ceo_rating=92, hiring_surge=True),
    Holding("FSLY", 10, reason="Leader in CDNs", is_founder_active=True, glassdoor_ceo_rating=100, hiring_surge=True),

    Holding("PTON", 10, reason="Leader in home fitness", is_founder_active=True, glassdoor_ceo_rating=91,
            hiring_surge=True),
    Holding("FIVN", 10, reason="Leader in contact center tech.", hiring_surge=True),
    Holding("CRWD", 10, reason="Leader in endpoint security, needed for WFH", hiring_surge=True),
    Holding("U", 10, reason="Leader in AR/VR", hiring_surge=True),

    # Medium conviction.
    Holding("NVDA", 5, reason="Leader in Machine learning", is_founder_active=True, glassdoor_ceo_rating=99),
    Holding("ZM", 5, reason="Leader in communication. Somewhat strong network effects.", is_founder_active=True,
            glassdoor_ceo_rating=98, hiring_surge=True),
    Holding("SE", 5, reason="Leader in Ecommerce in SE Asia", is_founder_active=True, glassdoor_ceo_rating=67),
    Holding("TTD", 5, reason="???", tactical="Slowly build up a position?", is_founder_active=True,
            glassdoor_ceo_rating=87),
    Holding("ROKU", 5, reason="Leader in home entertainment", is_founder_active=True, glassdoor_ceo_rating=78,
            hiring_surge=True),
    Holding("NET", 5, reason="Launching WFH solution.", hiring_surge=True),
    Holding("ZS", 5, reason="Security. Massive hiring surge.", hiring_surge=True),
    Holding("OKTA", 5, reason="Leader in IAM, needed for WFH"),
    Holding("DOCU", 5, reason="Leader in document management.", tactical="Slowly build up a position?",
            is_founder_active=True, glassdoor_ceo_rating=98),
    Holding("SQ", 5, reason="Leader in ECommerce payment solutions.", is_founder_active=True, glassdoor_ceo_rating=87),
    Holding("NIO", 5, reason="Leader in chinese EVs.", is_founder_active=True, glassdoor_ceo_rating=87),
    Holding("FRPT", 5, reason="Fresh food for pets."),
    Holding("TRUP", 5, reason="Insurance administrator for pets."),
    Holding("CHWY", 5, reason="More people are getting pets and seem to like chewy."),

    #
    # Holding("QQQ", -3, reason="Hedge."),
    Holding("WCLD", -1, reason="Hedge."),
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
