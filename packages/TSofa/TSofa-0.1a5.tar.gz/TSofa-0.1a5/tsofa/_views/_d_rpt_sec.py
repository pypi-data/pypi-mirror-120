# Local package imports.
from tsofa._views._base_d_rpt import Command as BC


class Command(BC):

    # Set the source, report, and date data endpoint for a time
    # resolution in seconds.
    default_endpoint = '/_design/d-rpt-sec/_view/d-rpt-sec/queries'


def main():
    Command.run()

