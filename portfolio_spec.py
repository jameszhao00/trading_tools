from portfolio_types import *

# Major themes:
# Stimulus delayed.

portfolio = Portfolio(long_leverage=100, longs=[
    Holding("PBW", reason="Clean energy"),
    Holding("DDOG", reason="Leader in production monitoring", is_founder_active=True, glassdoor_ceo_rating=93,
            hiring_surge=True),
    Holding("TWLO", reason="Leader in communication IaaS and call centers", is_founder_active=True,
            glassdoor_ceo_rating=92, hiring_surge=True),
    Holding("FSLY", reason="Leader in CDNs", is_founder_active=True, glassdoor_ceo_rating=100, hiring_surge=True),

    Holding("PTON", reason="Leader in home fitness", is_founder_active=True, glassdoor_ceo_rating=91,
            hiring_surge=True),
    Holding("FIVN", reason="Leader in contact center tech.", hiring_surge=True),
    Holding("CRWD", reason="Leader in endpoint security, needed for WFH", hiring_surge=True),

    # Medium conviction.
    Holding("NVDA", reason="Leader in Machine learning", is_founder_active=True, glassdoor_ceo_rating=99),
    Holding("ZM", reason="Leader in communication. Somewhat strong network effects.", is_founder_active=True,
            glassdoor_ceo_rating=98, hiring_surge=True),
    Holding("SE", reason="Leader in Ecommerce in SE Asia", is_founder_active=True, glassdoor_ceo_rating=67),
    Holding("TTD", reason="???", tactical="Slowly build up a position?", is_founder_active=True,
            glassdoor_ceo_rating=87),
    Holding("ROKU", reason="Leader in home entertainment", is_founder_active=True, glassdoor_ceo_rating=78,
            hiring_surge=True),
    Holding("NET", reason="Launching WFH solution.", hiring_surge=True),
    Holding("ZS", reason="Security. Massive hiring surge.", hiring_surge=True),
    Holding("OKTA", reason="Leader in IAM, needed for WFH"),
    Holding("DOCU", reason="Leader in document management.", tactical="Slowly build up a position?",
            is_founder_active=True, glassdoor_ceo_rating=98),
    Holding("SQ", reason="Leader in ECommerce payment solutions.", is_founder_active=True, glassdoor_ceo_rating=87),
    Holding("NIO", reason="Leader in chinese EVs.", is_founder_active=True, glassdoor_ceo_rating=87),
    Holding("FRPT", reason="Fresh food for pets."),
    Holding("TRUP", reason="Insurance administrator for pets."),
    Holding("CHWY", reason="More people are getting pets and seem to like chewy."),

    # Not enough history
    # Holding("U",  reason="Leader in AR/VR", hiring_surge=True),

    # Zillow CEO seems really MBA.
    Holding("ZG", reason="Leader in Home purchasing", is_founder_active=True, glassdoor_ceo_rating=93),
    Holding("SNAP", reason="Leader in teen social media", is_founder_active=True, glassdoor_ceo_rating=77),
    # Per glassdoor snap's culture is apparently really douchey.

    # Remote Productivity Leaders.
    # Holding("TEAM", reason="Leader in project management. There's strong network effects in project management. If "
    #                        "I'm used to JIRA I really don't want to switch to Asana.", is_founder_active=True,
    #         glassdoor_ceo_rating=97),
    Holding("SHOP", reason="Amazing Glassdoor reviews.", tactical="Slowly build up a position?"),

    # Holding("HUBS", 3, reason="Amazing Glassdoor reviews.", tactical="Slowly build up a position?", is_founder_active=True,
    #         glassdoor_ceo_rating=98),
    #
    # Holding("U", 3, reason="Leader in game/interactive experiences IaaS.", tactical="Slowly build up the position.",
    #         glassdoor_ceo_rating=92),
    # Holding("SNOW", 3, reason="Best product at data warehousing/analytics.", tactical="Slowly build up the position.",
    #         is_founder_active=True, glassdoor_ceo_rating=89),

    # ECommerce.
    # Why not Carvana? Because the CEO is a convicted felon.
    Holding("W", reason="Online furniture company.", tactical="Slowly build up a position.", is_founder_active=True,
            glassdoor_ceo_rating=57),
    Holding("RH", reason="Fancy home company."),
    # Holding("TSM", reason="Semiconductor company."),
    Holding("ITB", reason="Home construction."),
    Holding("LULU", reason="WFH Clothing."),
    Holding("AMZN", reason="Jeff bezos."),
    Holding("SPOT", reason="Music monopoly."),

    Holding("TXG", reason="CPOAX top 10 holding 9/30/2020."),
    Holding("CVNA", reason="CPOAX top 10 holding 9/30/2020."),
    Holding("COUP", reason="CPOAX top 10 holding 9/30/2020."),
    Holding("ISRG", reason="CPOAX top 10 holding 9/30/2020."),
    Holding("MDB", reason="CPOAX top 10 holding 9/30/2020."),
    Holding("UBER", reason="CPOAX top 10 holding 9/30/2020."),
    Holding("VEEV", reason="CPOAX top 10 holding 9/30/2020."),

    Holding("NVTA", reason="ARKK top 10 holding 9/30/2020."),
    Holding("CRSP", reason="ARKK top 10 holding 9/30/2020."),
    Holding("PRLB", reason="ARKK top 10 holding 9/30/2020."),
    Holding("WORK", reason="ARKK top 10 holding 9/30/2020."),
    Holding("TSLA", reason="ARKK top 10 holding 9/30/2020."),

    Holding("VXX", reason="Hedge")
    # Holding("WMT", reason="Big chain store."),
    # Holding("JPM", reason="Fancy home company."),
    # Holding("GS", reason="Fancy home company."),
], shorts=[
    # Shorts.
    # Tech.
    Holding("CSCO", reason="Things are moving to the cloud. Less need for physical network gear."),
    Holding("INTC", reason="Less desktops. Server chips are moving to ARM/in house processors/GPUs."),
    Holding("DBX", reason="Google/Microsoft/... cloud storage owning this.", is_founder_active=True),
    Holding("BOX", reason="Google/Microsoft/... cloud storage owning this.", is_founder_active=True),
    Holding("NLOK",
            reason="Newer devices do not need consumer facing antivirus. How many people buy consumer fraud prevention?"),
    Holding("CLDR", reason="Cloudera's been left behind by companies like Snowflake."),
    Holding("IBM", reason="It's IBM"),
    Holding("VRSN", reason="Verisign is massively rent seeking. Doesn't innovate."),
    #
    # # Energy and finance.
    Holding("XLE"),
    # Holding("XLF", -7),
    # # Tobacco stocks
    Holding("MO", reason="Smoking on the decline"),
    Holding("PM", reason="Smoking on the decline"),
])
