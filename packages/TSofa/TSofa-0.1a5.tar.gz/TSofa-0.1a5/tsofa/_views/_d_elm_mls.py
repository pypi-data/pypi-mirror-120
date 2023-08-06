# Standard library imports.
import datetime

# Local package imports.
from tsofa._views._base_d_elm import Command as BC


class Command(BC):

    # Specify the default timedelta to use to include or exclude the
    # start or end of a resampled date ranges.
    timedelta = datetime.timedelta(microseconds = 1000)

    # Set the source, report, element, and date data endpoint for a
    # date and time resolution in milliseconds.
    default_endpoint = '/_design/d-elm-mls/_view/d-elm-mls/queries'


def main():
    Command.run()

