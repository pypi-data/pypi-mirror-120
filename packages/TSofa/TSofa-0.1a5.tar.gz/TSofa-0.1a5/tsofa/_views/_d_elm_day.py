# Standard library imports.
import datetime

# Local package imports.
from tsofa._views._base import TMPLS_DATES
from tsofa._views._base_d_elm import Command as BC


class Command(BC):

    # Specify the acceptable date templates to accept only dates.
    tmpls = TMPLS_DATES
    tmpls_dates = TMPLS_DATES

    # Specify the allowable resampling frequency.
    rfrqs = ('yly', 'mly',)

    # Specify the default timedelta to use to include or exclude the
    # start or end of a resampled date ranges.
    timedelta = datetime.timedelta(days = 1)

    # Set the source, report, element, and date data endpoint for a
    # date resolution in days.
    default_endpoint = '/_design/d-elm-day/_view/d-elm-day/queries'


def main():
    Command.run()

