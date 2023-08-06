# Standard library imports.
import argparse
import datetime
import json

# pytz package imports.
import pytz

# requests package imports.
import requests

# Two-Percent package imports.
from twopct.base import Command as BC

# Local package imports.
from tsofa.utils import gen_date_key as gdk
from tsofa.utils import parse_date_key as pdk


# Parse date strings using the list of possible formats.
TMPLS = [
    '%Y-%m-%dT%H:%M:%S.%f',
    '%Y-%m-%dT%H:%M:%S',
    '%Y-%m-%dT%H:%M',
    '%Y-%m-%dT%H',
    '%Y-%m-%d',
    '%Y%m%dT%H%M%S.%f',
    '%Y%m%dT%H%M%S',
    '%Y%m%dT%H%M',
    '%Y%m%dT%H',
    '%Y%m%d']

TMPLS_DATES = ['%Y-%m-%d', '%Y%m%d']



# The default time zone string, which is "UTC".  Used to add the tzinfo
# object to "datetime.datetime" objects if another time zone is not
# specified.
TIME_ZONE = 'UTC'

# Define some date types.
TYPE_DA = type(datetime.date.today())
TYPE_DT = type(datetime.datetime.now())


class Command(BC):

    # Specify the acceptable datetime and date templates used to parse
    # a command line date argument.
    tmpls = TMPLS
    tmpls_dates = TMPLS_DATES

    # Specify a list of parameter names accepted by the query method.
    pnames = []

    # Define a default CouchDB view endpoint used in the request method.
    default_endpoint = ''

    # Returned database view keys are an array.  Specify the index where
    # the key should be sliced so that the key contains only the date
    # components.
    key_date_index = 0

    def _clean_date(self, date, tz):

        if 'datetime.datetime' in str(type(date)):

            try:
                output = pytz.timezone(tz).localize(date)

            except:
                output = pytz.UTC.localize(date)

        else:
            output = date

        return output

    def arg_date(self, str_value):

        date = None
        tmpl = None
        count = 0

        while count < len(self.tmpls):

            try:
                date = datetime.datetime.strptime(str_value, self.tmpls[count])

            except:
                date = None

            if date != None:

                tmpl = TMPLS[count]
                count = len(TMPLS)

            count += 1

        if date is None:
            raise argparse.ArgumentTypeError(
                '{} is not a valid date'.format(str_value))

        elif tmpl in self.tmpls_dates:
            date = date.date()

        return date

    def arg_param(self, param):

        # Get the time zone string.
        tz = self.arg_tz(param.get('tz', TIME_ZONE))

        if 'sdate' in param.keys():
            param['sdate'] = self._clean_date(
                self.arg_date(param['sdate']), tz)

        else:
            raise argparse.ArgumentTypeError(
                'An "sdate" date parameter must be included')

        if 'edate' in param.keys():
            param['edate'] = self._clean_date(
                self.arg_date(param['edate']), tz)

        else:
            raise argparse.ArgumentTypeError(
                'An "edate" date parameter must be included')

        return param

    def arg_params(self, str_value):

        params = None

        try:
            params = json.loads(str_value)

        except Exception as e:
            raise argparse.ArgumentTypeError('Invalid JSON')

        if type(params) == type([]):

            counter = 0

            while counter < len(params):

                if type(params[counter]) == type({}):
                    params[counter] = self.arg_param(params[counter])

                else:
                    raise argparse.ArgumentTypeError(
                        'Contents of params list must be dictionaries')

                counter += 1

        else:
            raise argparse.ArgumentTypeError(
                'The params argument must be a list')

        return params

    def arg_tz(self, str_value):

        try:
            tz = pytz.timezone(str_value)

        except:
            raise argparse.ArgumentTypeError(
                '{} is not a valid time zone'.format(str_value))

        return str_value

    def add_arguments(self, parser):

        parser.add_argument(
            'db',
            type = str,
            help = 'URL to a CouchDB database containing timeseries data')
        parser.add_argument(
            'params',
            type = self.arg_params,
            help = 'A list of JSON parameters defining multiple output')

        return None

    def dumps(self, value, **kwargs):
        return json.dumps(value)

    def gen_queries(self, params):

        # Define the query dictionary needed to perform multiple data
        # requests using a single call to the database.
        queries = {'queries': []}

        for p in params:

            # If an item in the params list is not a dictionary, then
            # create an empty dictionary.
            if type(p) != type({}):
                p = {}

            qka = {}

            for k in self.pnames:
                qka[k] = p.get(k, '')

            queries['queries'].append(self.gen_query(**qka))

        return queries

    def handle(self, *args, **kwargs):

        # Return database data using this variable.
        data = []

        # Generate the queries from the given parameters list.
        queries = self.gen_queries(kwargs['params'])

        # Make the data request.
        results = self.request(kwargs['db'], queries)

        if results is not None:

            # The counter to index into the params list.
            c1 = 0

            while c1 < len(kwargs['params']):

                p = kwargs['params'][c1]
                sdate = p.get('sdate', None)

                # Define the default time zone value.  THis value may
                # be overridden based upon if the "sdate" param is a
                # datetime object and it has a "tzinfo" object.
                tz = TIME_ZONE

                if sdate is not None:
                    if type(sdate) == TYPE_DT:
                        if sdate.tzinfo is not None:
                            tz = str(sdate.tzinfo)

                # Store the parsed date and value from the results rows.
                tmp = []

                for r in results['results'][c1]['rows']:
                    #tmp.append([self.parse_date_key(r['key'], tz), r['value']])
                    tmp.append(self.parse_row(r, tz))

                # Add processed rows to the data output.
                data.append(tmp)

                c1 += 1

        return data

    def parse_date_key(self, key, tz):
        """Returns a date string from the date component of a row key.

        """
        # Slice the key list (array) to contain only the date component,
        # then pass the sliced key to the utility function.
        try:
            key = key[self.key_date_index:]

        except:
            key = []

        return pdk(key, tz, as_str = True)

    def parse_row(self, row, tz):

        date = self.parse_date_key(row['key'], tz)
        valu = row['value']

        return [date, valu]

    def request(self, db, queries, endpoint = None):

        # Set the view endpoint.
        _ep = self.default_endpoint

        if type(endpoint) == type(''):
            _ep = endpoint

        # Perform the database requests.  If any one of the requests
        # fail, no data is returned.
        results = {}

        try:
            results = requests.post(
                db + _ep,
                headers = {'Content-Type': 'application/json'},
                data = json.dumps(queries),
                timeout = 30.0).json()

        except Exception as e:

            results = None
            self.stderr(str(e))

        return results

    @staticmethod
    def gen_date_key(date):
        return gdk(date)

    @staticmethod
    def gen_query(**kwargs):
        return {}

