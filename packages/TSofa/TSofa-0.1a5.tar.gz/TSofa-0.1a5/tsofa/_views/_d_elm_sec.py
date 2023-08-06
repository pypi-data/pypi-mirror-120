# Local package imports.
from tsofa._views._base_d_elm import Command as BC


class Command(BC):

    # Specify the allowable resampling frequency.
    rfrqs = ('yly', 'mly', 'dly', 'hly', 'mny',)

    # Set the source, report, element, and date data endpoint for a
    # time resolution in seconds.
    default_endpoint = '/_design/d-elm-sec/_view/d-elm-sec/queries'


def main():
    Command.run()

