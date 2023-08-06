# Local package imports.
from tsofa._views._base_d_doc import Command as BC


class Command(BC):

    # Set the source and date data endpoint for a time resolution in
    # seconds.
    default_endpoint = '/_design/d-doc-sec/_view/d-doc-sec/queries'


def main():
    Command.run()

