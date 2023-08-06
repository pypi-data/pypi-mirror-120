# Local package imports.
from tsofa._views._base_s_atr import Command as BC


class Command(BC):

    # Set the source, attribute, and date metadata endpoint for a time
    # resolution in seconds.
    default_endpoint = '/_design/s-atr-sec/_view/s-atr-sec/queries'


def main():
    Command.run()

