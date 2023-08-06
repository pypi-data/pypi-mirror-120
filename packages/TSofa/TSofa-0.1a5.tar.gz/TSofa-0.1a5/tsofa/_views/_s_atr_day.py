# Local package imports.
from tsofa._views._base import TMPLS_DATES
from tsofa._views._base_s_atr import Command as BC


class Command(BC):

    # Specify the acceptable date templates to accept only dates.
    tmpls = TMPLS_DATES
    tmpls_dates = TMPLS_DATES

    # Set the source, attribute, and date metadata endpoint for a date
    # resolution in days.
    default_endpoint = '/_design/s-atr-day/_view/s-atr-day/queries'


def main():
    Command.run()

