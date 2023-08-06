# Local package imports.
from tsofa._views._base_d_doc import Command as BC


class Command(BC):

    # Set the source and date data endpoint for a date resolution in
    # days.
    default_endpoint = '/_design/d-doc-day/_view/d-doc-day/queries'


def main():
    Command.run()

