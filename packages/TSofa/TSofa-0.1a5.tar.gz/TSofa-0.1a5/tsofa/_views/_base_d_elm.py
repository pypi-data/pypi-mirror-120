# Standard library imports.
import calendar
import copy
import datetime
from argparse import ArgumentTypeError as ATE

# Local package imports.
from tsofa._views._base import TYPE_DA
from tsofa._views._base import TYPE_DT
from tsofa._views._base import Command as BC


# List the parameter names used to construct a database query.
PNAMES = ('sid', 'rpt', 'elm', 'sdate', 'edate', 'desc', 'limit', 'reduce')


class Command(BC):

    # Set the templates for dates to empty.  Only datetimes will be
    # parsed.
    tmpls_dates = []

    # Specify the allowable resampling frequency.
    rfrqs = ('yly', 'mly', 'dly', 'hly', 'mny', 'sly',)

    # Specify the default timedelta to use to include or exclude the
    # start or end of a resampled date ranges.
    timedelta = datetime.timedelta(seconds = 1)

    # The gen_query method below accepts only the argument names defined
    # in the above "PNAMES".
    pnames = PNAMES

    # The Javascript view emits keys containing the source ID, data
    # report ID, the data element ID and a date component.  The value
    # emitted should be a numerical value.
    #
    # THIS IS NOT A VALID ENDPOINT.  The endpoint is shown as an
    # example.  Set the correct endpoint in the child classes.
    default_endpoint = '/_design/base-d-elm/_view/base-d-elm/queries'

    # The date component of the returned keys starts after the source
    # ID, the data report ID, and the data element ID values.
    key_date_index = 3

    def __find_rfrq(self, rc):

        rfrq = None

        count = 0

        while count < len(self.rfrqs):

            if self.rfrqs[count] in rc:

                rfrq = self.rfrqs[count]
                count = len(self.rfrqs)

            count += 1

        return rfrq

    def __gen_params(self, param):

        # A list of expanded parameters based on the number of date and
        # time intervals between the start and end date ranges.
        expanded = []

        # This is the resampling code, specifying the type of
        # resampling and the inclusion/exclusion rules.
        rc = str(param.get('rsmp', ''))

        # Determine if the reported date for the resampled data should
        # be at the end of the interval.
        eoi = False

        if rc.startswith('-'):

            rc = rc[1:]
            eoi = True

        # Get the reference to the start date in the params dictionary.
        sdate = param['sdate']

        # Generate a param dictionary for every given day.
        while sdate <= param['edate']:

            # Generate a new parameters dictionary.
            np = self.__np(param)

            # Specifies that the given day is the end of the daily reporting
            # period, so the day is used as the endpoint of the day data
            # request.
            if eoi == True:

                sd = sdate - param['td']
                ed = sdate

            else:

                sd = sdate
                ed = sdate + param['td']

            # Adjust the start and end date enpoints if necessary, and
            # add to the new params.
            np.update(self.__se_adj(rc, sd, ed))

            # Finally add the new parameter dictionary to the params
            # list.
            expanded.append(np)

            # Increment current date of the loop by the timedelta given
            # in the param dictionary.
            sdate += param['td']

        return expanded

    def __np(self, param):

        np = {'reduce': True}

        for k in ('sid', 'rpt', 'elm',):
            np[k] = param[k]

        return np

    def __se_adj(self, rc, sd, ed):

        # Determine if the endpoints of the time interval should be
        # included in the resampled data set for the given interval.
        if rc.startswith('X') == True:
            sd += self.timedelta

        if rc.endswith('X') == True:
            ed -= self.timedelta

        return {'sdate': sd, 'edate': ed}

    def arg_param(self, param):

        param = BC.arg_param(self, param)

        for a in ('sid', 'rpt', 'elm',):

            if a in param.keys():
                if type(param[a]) != type(''):
                    raise ATE('{} must be string'.format(a))

            else:
                raise ATE('{} is required'.format(a))

        for a in ('desc', 'reduce'):
            if type(param.get(a, False)) != type(True):
                raise ATE('{} must be a boolean value'.format(a))

        if type(param.get('limit', 0)) != type(0):
            raise ATE('limit must be an integer')

        if type(param.get('rsmp', '')) != type(''):
            raise ATE('rsmp must be a string literal')

        return param

    def exp_yly(self, param):

        # A list of expanded parameters based on the number of years
        # between the start and end date ranges.
        expanded = []

        # This is the resampling code, specifying the type of
        # resampling and the inclusion/exclusion rules.
        rc = str(param.get('rsmp', ''))

        # Determine if the reported date for the resampled data should
        # be at the end of the interval.
        eoi = False

        if rc.startswith('-'):

            rc = rc[1:]
            eoi = True

        # Get the start and end date(time) parameters.
        psd = param['sdate']
        ped = param['edate']

        # Get the start and end dates (datetimes).
        if (type(psd) == TYPE_DA) and (type(ped) == TYPE_DA):

            sd = datetime.date(psd.year, 1, 1)
            ed = datetime.date(ped.year, 1, 1)

        elif (type(psd) == TYPE_DT) and (type(ped) == TYPE_DT):

            sd = psd.tzinfo.localize(datetime.datetime(psd.year, 1, 1))
            ed = ped.tzinfo.localize(datetime.datetime(ped.year, 1, 1))

        else:

            sd = None
            ed = None

        if sd and ed:

            while sd <= ed:

                # Generate a new parameters dictionary.
                np = self.__np(param)

                # Adjust the start and end dates by a year, depending
                # upon the state of the "end of interval" variable.
                if eoi == True:

                    # If the previous year is a leap year, then subtract
                    # 366 days from the start date.
                    if calendar.isleap(sd.year - 1) == True:
                        _sd = sd - datetime.timedelta(days = 366)

                    else:
                        _sd = sd - datetime.timedelta(days = 365)

                    _ed = sd

                else:

                    _sd = sd

                    # If the current year is a leap year, then add 366
                    # days to the start date.
                    if calendar.isleap(sd.year) == True:
                        _ed = sd + datetime.timedelta(days = 366)

                    else:
                        _ed = sd + datetime.timedelta(days = 365)

                # Adjust the start and end date enpoints if necessary,
                # and add to the new params.
                np.update(self.__se_adj(rc, _sd, _ed))

                # Finally add the new parameter dictionary to the params
                # list.
                expanded.append(np)

                if type(sd) == TYPE_DA:
                    sd = datetime.date(sd.year + 1, 1, 1)

                else:
                    sd = sd.tzinfo.localize(
                        datetime.datetime(sd.year + 1, 1, 1))

        return expanded

    def exp_mly(self, param):

        # A list of expanded parameters based on the number of months
        # between the start and end date ranges.
        expanded = []

        # This is the resampling code, specifying the type of
        # resampling and the inclusion/exclusion rules.
        rc = str(param.get('rsmp', ''))

        # Determine if the reported date for the resampled data should
        # be at the end of the interval.
        eoi = False

        if rc.startswith('-'):

            rc = rc[1:]
            eoi = True

        # Get the start and end date(time) parameters.
        psd = param['sdate']
        ped = param['edate']

        # Get the start and end dates (datetimes).
        if (type(psd) == TYPE_DA) and (type(ped) == TYPE_DA):

            sd = datetime.date(psd.year, psd.month, 1)
            ed = datetime.date(ped.year, ped.month, 1)

        elif (type(psd) == TYPE_DT) and (type(ped) == TYPE_DT):

            sd = psd.tzinfo.localize(datetime.datetime(psd.year, psd.month, 1))
            ed = ped.tzinfo.localize(datetime.datetime(ped.year, ped.month, 1))

        else:

            sd = None
            ed = None

        if sd and ed:

            while sd <= ed:

                # Generate a new parameters dictionary.
                np = self.__np(param)

                # Adjust the start and end dates by a month depending
                # upon the state of the "end of interval" variable.
                if eoi == True:

                    tmp = sd - datetime.timedelta(days = 1)
                    _sd = sd - datetime.timedelta(
                        days = calendar.monthrange(tmp.year, tmp.month)[1])
                    _ed = sd

                else:

                    _sd = sd
                    _ed = sd + datetime.timedelta(
                        days = calendar.monthrange(sd.year, sd.month)[1])

                # Adjust the start and end date enpoints if necessary,
                # and add to the new params.
                np.update(self.__se_adj(rc, _sd, _ed))

                # Finally add the new parameter dictionary to the params
                # list.
                expanded.append(np)

                sd += datetime.timedelta(
                    days = calendar.monthrange(sd.year, sd.month)[1])

        return expanded

    def exp_dly(self, p):

        # Adjust the start and end datetime objects to zero time values.
        for k in ('sdate', 'edate',):
            p[k] = p[k].tzinfo.localize(
                datetime.datetime(p[k].year, p[k].month, p[k].day))

        # Add the timedelta to the new params dictionary.
        p['td'] = datetime.timedelta(days = 1)

        return self.__gen_params(p)

    def exp_hly(self, p):

        # Adjust the start and end datetime objects to the bottom of
        # the given hour.
        for k in ('sdate', 'edate',):
            p[k] = p[k].tzinfo.localize(
                datetime.datetime(p[k].year, p[k].month, p[k].day, p[k].hour))

        # Add the timedelta to the new params dictionary.
        p['td'] = datetime.timedelta(seconds = 3600)

        return self.__gen_params(p)

    def exp_mny(self, p):

        # Adjust the start and end datetime objects to the bottom of
        # the given minute.
        for k in ('sdate', 'edate',):
            p[k] = p[k].tzinfo.localize(
                datetime.datetime(
                    p[k].year, p[k].month, p[k].day, p[k].hour, p[k].minute))

        # Add the timedelta to the new params dictionary.
        p['td'] = datetime.timedelta(seconds = 60)

        return self.__gen_params(p)

    def exp_sly(self, p):

        # Adjust the start and end datetime objects to the bottom of
        # the given second.
        for k in ('sdate', 'edate',):
            p[k] = p[k].tzinfo.localize(
                datetime.datetime(
                    p[k].year,
                    p[k].month,
                    p[k].day,
                    p[k].hour,
                    p[k].minute,
                    p[k].second))

        # Add the timedelta to the new params dictionary.
        p['td'] = datetime.timedelta(seconds = 1)

        return self.__gen_params(p)

    def handle(self, *args, **kwargs):

        # The return value.
        data = []

        # Depending on the reduction code, each given param dictionary
        # will be expanded to include every time interval between the
        # original start and end dates.
        expanded_params = []

        for param in kwargs['params']:

            rfrq = self.__find_rfrq(param.get('rsmp', ''))

            if rfrq is not None:

                # Get resampling method from the class instance.
                method = getattr(self, 'exp_' + rfrq, None)

                if callable(method) == True:
                    expanded = method(copy.deepcopy(param))

                else:
                    expanded = []

                # Add the list of expanded parameters to the new
                # parameters list.
                expanded_params.extend(expanded)

                # Set the count of expanded parameters in the original
                # params list.
                param['count'] = len(expanded)

            else:

                # If a resampling method is not defined, then add the
                # "un-expanded" param dictionary to the new list.  Set
                # the count of expanded params to 1.
                expanded_params.append(param)
                param['count'] = 1

        # Call the parent method.
        _data = super(Command, self).handle(
            **{'db': kwargs['db'], 'params': expanded_params})

        # Increment this counter based upon the count argument added to
        # the original params dictionaries.
        cd = 0

        for param in kwargs['params']:

            # Create a list of data that, at the end of this loop, will
            # be added to the output list.
            _tmp = []

            # Iterate over the parent method's data output based upon
            # the number of date and time intervals used for resampling.
            for i in range(cd, cd + param['count']):

                # Get a single date and time interval parameter from the
                # expanded list of params.
                ep = expanded_params[i]

                # Loop over the returned values for the expanded params.
                for j in _data[i]:

                    _date = j[0]

                    if _date == None:

                        _date = ep['sdate']

                        if str(param.get('rsmp', '')).startswith('-'):

                            _date = ep['edate']

                            if str(param.get('rsmp', '')).endswith('X'):
                                _date += self.timedelta

                        elif str(param.get('rsmp', '')).startswith('X'):
                            _date -= self.timedelta

                        ################################################
                        # NEED TO FIX THIS IN THE CASE OF MILLISECOND
                        # RESOLUTION OR DAY RESOLUTION!!!
                        ################################################
                        _date = _date.strftime('%Y-%m-%dT%H:%M:%S')

                    # Add to the current data list.
                    _tmp.append([_date, j[1]])

            # Add the list of data to the output list.
            data.append(_tmp)

            cd += param['count']

        return data

    @staticmethod
    def gen_query(sid, rpt, elm, sdate, edate, **kwargs):

        query = {'reduce': 'false'}

        # Create the start and end key "arrays" for the query,
        # populating the first three elements with the source ID,
        # report and data element ID values.
        query['startkey'] = [sid, rpt, elm]
        query['endkey'] = [sid, rpt, elm]

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

        # If the reduction flag is not set in the keyword arguments,
        # then specify that the reduce option is false.
        if kwargs.get('reduce', False) == True:
            query['reduce'] = 'true'

        return query

