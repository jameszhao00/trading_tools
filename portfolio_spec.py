from portfolio_types import *

# Major themes:
# Stimulus delayed.

portfolio = Portfolio(long_leverage=100, short_leverage=50, holdings=[
    # Longs

    # Growth
    # What to look for:
    # Small/medium Growth.
    Holding("SQ", 10, reason="Leader in ECommerce payment solutions."),
    Holding("DDOG", 10, reason="Leader in production monitoring"),
    Holding("TWLO", 10, reason="Leader in communication IaaS"),
    Holding("SE", 10, reason="Leader in Ecommerce in SE Asia"),

    # Remote Productivity Leaders.
    Holding("TEAM", 5, reason="Leader in project management. There's strong network effects in project management. If "
                              "I'm used to JIRA I really don't want to switch to Asana."),
    Holding("ZM", 5, reason="Leader in communication. Somewhat strong network effects."),
    Holding("PTON", 5, reason="Leader in home fitness", tactical="Buy more once it drops a bit."),
    Holding("U", 4, reason="Leader in game/interactive experiences IaaS.", tactical="Slowly build up the position."),
    Holding("SNOW", 4, reason="Best product at data warehousing/analytics.", tactical="Slowly build up the position."),

    # ECommerce.
    Holding("W", 4, reason="Online furniture company.", tactical="Slowly build up a position."),
    Holding("ETSY", 5, reason="Leader in quirky online shopping. Different than amazon. Great moat."),

    Holding("TTD", 3, reason="???", tactical="Slowly build up a position?"),

    Holding("PBW", 10, reason="Clean energy"),
    Holding("ICLN", 5, reason="Clean energy"),

    # Shorts.
    # Tech.
    Holding("CSCO", -5, reason="Things are moving to the cloud. Less need for physical network gear."),
    Holding("DBX", -2, reason="Google/Microsoft/... cloud storage owning this."),
    Holding("BOX", -2, reason="Google/Microsoft/... cloud storage owning this."),
    Holding("NLOK", -2,
            reason="Newer devices do not need consumer facing antivirus. How many people buy consumer fraud prevention?"),
    Holding("CLDR", -2, reason="Cloudera's been left behind by companies like Snowflake."),
    Holding("IBM", -5, reason="It's IBM"),

    # Energy and finance.
    Holding("XLE", -12),
    Holding("XLF", -8),
    # Tobacco stocks
    Holding("MO", -3, reason="Smoking on the decline"),
    Holding("PM", -3, reason="Smoking on the decline"),
])
