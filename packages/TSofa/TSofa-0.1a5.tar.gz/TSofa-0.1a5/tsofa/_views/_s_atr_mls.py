# Local package imports.
from tsofa._views._base_s_atr import Command as BC


class Command(BC):

    # Set the source, attribute, and date metadata endpoint for a time
    # resolution in milliseconds.
    default_endpoint = '/_design/s-atr-mls/_view/s-atr-mls/queries'


def main():
    Command.run()

