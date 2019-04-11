"""
A custom calendar that can be used to start up the application
"""


from sleepcounter.time.calendar import Calendar
from sleepcounter.time.event import SpecialDay, Anniversary

_DEFAULT_SLEEPS_TO_COUNT = 20

EVENTS = [
    Anniversary(
        name='Bonfire Night',
        month=11,
        day=5,
        sleeps=_DEFAULT_SLEEPS_TO_COUNT
    ),
    Anniversary(
        name='Halloween',
        month=10,
        day=31,
        sleeps=_DEFAULT_SLEEPS_TO_COUNT
    ),
    Anniversary(
        name='Christmas',
        month=12,
        day=25,
    ),
    Anniversary(name='Evie\'s Birthday', month=8, day=3),
    Anniversary(name='Felix\'s Birthday', month=6, day=16),
    SpecialDay(
        name='Legoland',
        year=2019,
        month=4,
        day=27,
        sleeps=_DEFAULT_SLEEPS_TO_COUNT
    ),
    Anniversary(
        name='Gagga\'s Birthday',
        month=3,
        day=7,
        sleeps=_DEFAULT_SLEEPS_TO_COUNT
    ),
    Anniversary(
        name='Uncle Bens\'s Birthday',
        month=3,
        day=17,
        sleeps=_DEFAULT_SLEEPS_TO_COUNT
    ),
    Anniversary(
        name='Grandad Ian\'s Birthday',
        month=4,
        day=24,
        sleeps=_DEFAULT_SLEEPS_TO_COUNT
    ),
    Anniversary(
        name='Nannay\'s Birthday',
        month=5,
        day=11,
        sleeps=_DEFAULT_SLEEPS_TO_COUNT
    ),
    SpecialDay(
        name='Easter',
        year=2019,
        month=4,
        day=21,
        sleeps=_DEFAULT_SLEEPS_TO_COUNT
    ),
    Anniversary(
        name='Fifi\'s Birthday',
        month=12,
        day=28,
        sleeps=_DEFAULT_SLEEPS_TO_COUNT
    ),
    Anniversary(
        name='Jesse\'s Birthday',
        month=2,
        day=12,
        sleeps=_DEFAULT_SLEEPS_TO_COUNT
    ),
    Anniversary(
        name='Totty\'s Birthday',
        month=2,
        day=14,
        sleeps=_DEFAULT_SLEEPS_TO_COUNT
    ),
]
CUSTOM_DIARY = Calendar(EVENTS)
