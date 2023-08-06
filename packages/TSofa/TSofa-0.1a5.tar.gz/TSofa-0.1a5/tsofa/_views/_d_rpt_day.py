# Local package imports.
from tsofa._views._base import TMPLS_DATES
from tsofa._views._base_d_rpt import Command as BC


class Command(BC):

    # Specify the acceptable date templates to accept only dates.
    tmpls = TMPLS_DATES
    tmpls_dates = TMPLS_DATES

    # Set the source, report, and date data endpoint for a date
    # resolution in days.
    default_endpoint = '/_design/d-rpt-day/_view/d-rpt-day/queries'


def main():
    Command.run()

