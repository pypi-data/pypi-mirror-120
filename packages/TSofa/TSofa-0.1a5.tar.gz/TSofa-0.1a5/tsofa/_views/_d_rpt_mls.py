# Local package imports.
from tsofa._views._base_d_rpt import Command as BC


class Command(BC):

    # Set the source, report, and date data endpoint for a time
    # resolution in milliseconds.
    default_endpoint = '/_design/d-rpt-mls/_view/d-rpt-mls/queries'


def main():
    Command.run()

