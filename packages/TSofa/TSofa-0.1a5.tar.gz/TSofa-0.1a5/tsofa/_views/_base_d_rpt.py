# Standard library imports.
from argparse import ArgumentTypeError as ATE

# Local package imports.
from tsofa._views._base import Command as BC


class Command(BC):

    # Set the templates for dates to empty.  Only datetimes will be
    # parsed.
    tmpls_dates = []

    # The gen_query method below accepts only these argument names.
    pnames = ('sid', 'rpt', 'sdate', 'edate', 'desc', 'limit',)

    # The Javascript view emits keys containing the source ID, data
    # report ID, and a date component.  The value emitted should be a
    # Javascript object.
    #
    # THIS IS NOT A VALID ENDPOINT.  The endpoint is shown as an
    # example.  Set the correct endpoint in the child classes.
    default_endpoint = '/_design/base-d-rpt/_view/base-d-rpt/queries'

    # The date component of the returned keys starts after the source
    # ID and data report ID values.
    key_date_index = 2

    def arg_param(self, param):

        param = BC.arg_param(self, param)

        for a in ('sid', 'rpt',):

            if a in param.keys():
                if type(param[a]) != type(''):
                    raise ATE('{} must be string'.format(a))

            else:
                raise ATE('{} is required'.format(a))

        for a in ('desc', 'summarize'):
            if type(param.get(a, False)) != type(True):
                raise ATE('{} must be a boolean value'.format(a))

        if type(param.get('limit', 0)) != type(0):
            raise ATE('limit must be an integer')

        return param

    def handle(self, *args, **kwargs):

        data = []

        _data = super(Command, self).handle(*args, **kwargs)

        counter = 0

        for param in kwargs['params']:

            if param.get('summarize', False) == True:
                data.append(self.summarize(_data[counter]))

            else:
                data.append(_data[counter])

            counter += 1

        return data

    @staticmethod
    def gen_query(sid, rpt, sdate, edate, **kwargs):

        query = {'reduce': 'false'}

        # Create the start and end key "arrays" for the query,
        # populating the first three elements with the source ID
        # and report ID values.
        query['startkey'] = [sid, rpt]
        query['endkey'] = [sid, rpt]

        if kwargs.get('desc', False) == True:

            query['startkey'] += BC.gen_date_key(edate) + ['\ufff0']
            query['endkey'] += BC.gen_date_key(sdate)
            query['descending'] = 'true'

        else:

            query['startkey'] += BC.gen_date_key(sdate)
            query['endkey'] += BC.gen_date_key(edate) + ['\ufff0']

        # Limit the output to a given number of JSON documents.
        if type(kwargs.get('limit', None)) == type(0):
            if kwargs['limit'] > 0:
                query['limit'] = kwargs['limit']

        return query

    @staticmethod
    def summarize(lister):

        smry = {}

        for row in lister:

            for vbl in row[1].keys():

                value = row[1][vbl]
                date = row[0]

                if type(row[1][vbl]) == type({}):

                    if 'value' in row[1][vbl].keys():

                        value = row[1][vbl]['value']

                        if 'date' in row[1][vbl].keys():
                            date = row[1][vbl]['date']

                if type(value) in (type(0), type(0.0)):

                    if vbl not in smry.keys():
                        smry[vbl] = {
                            'max': {'value': value, 'date': date},
                            'min': {'value': value, 'date': date},
                            'avg': None,
                            'sum': 0,
                            'count': 0}

                    if value > smry[vbl]['max']['value']:

                        smry[vbl]['max']['value'] = value
                        smry[vbl]['max']['date'] = date

                    if value < smry[vbl]['min']['value']:

                        smry[vbl]['min']['value'] = value
                        smry[vbl]['min']['date'] = date

                    smry[vbl]['sum'] += value
                    smry[vbl]['count'] += 1

        for vbl in smry.keys():
            if smry[vbl]['count'] > 0:
                smry[vbl]['avg'] = smry[vbl]['sum'] / smry[vbl]['count']

        return smry

