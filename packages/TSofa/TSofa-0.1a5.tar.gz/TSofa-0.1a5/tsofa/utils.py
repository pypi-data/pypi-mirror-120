# Standard library imports.
import datetime
import random

# pytz package imports.
import pytz

# requests package imports.
import requests


def find_db(urls):

    # If an active CouchDB database is found, then this value will
    # be set to the URL value of the database.
    db = None

    # If the length of the urls is greater than zero, then continue
    # to attempt to find an active database.  Otherwise, do nothing
    # and return None.
    if len(urls) > 0:

        # Choose a random database from the given list.
        db_temp = random.choice(urls)
        db_alive = False

        try:

            r = requests.get(db_temp, timeout = 30.0)

            if r.status_code == 200:
                if r.json().get('db_name') is not None:
                    db_alive = True

        except:
            pass

        if db_alive == True:
            db = db_temp

        else:

            reduced_urls = []

            for url in urls:
                if url != db_temp:
                    reduced_urls.append(url)

            # Recursion, Yay!
            db = find_db(reduced_urls)

    return db


def gen_date_key(date):

    # Determine if the given date parameter is a "datetime.date"
    # object, or a "datetime.datetime" object.
    #if 'datetime.date' in str(type(date)):
    if type(date) == type(datetime.date.today()):

        # Format and evaluate the UTC date as list.
        tmpl = '["%Y","%m","%d"]'
        key = eval(date.strftime(tmpl))

    #elif 'datetime.datetime' in str(type(date)):
    elif type(date) == type(datetime.datetime.now()):

        # If the given "datetime.datetime" does not have a set
        # tzinfo object, then set the tzinfo as a "pytz.UTC" object.
        if date.tzinfo == None:
            date = pytz.UTC.localize(date)

        # Adjust the "datetime.datetime" to a UTC time zone.
        date = date.astimezone(pytz.UTC)

        # Format and evaluate the UTC date as list.
        tmpl = '["%Y","%m","%d","%H","%M","%S"]'
        key = eval(date.strftime(tmpl))

        # Get the nearest milliseconds from the microsecond
        # attribute of the "datetime.datetime" object.  Only
        # do so if the microseconds are greater than or equal to
        # 1000, or one millisecond.
        if date.microsecond >= 1000:

            ms = int(round(date.microsecond / 1000, 0))

            # Create a zero padded string of milliseconds to add to
            # the key.
            if ms < 10:
                key.append('00' + str(ms))

            elif ms < 100:
                key.append('0' + str(ms))

            else:
                key.append(str(ms))

    else:
        key = []

    return key


def parse_date_key(key, tz, as_str = False):
    """Parse the date component of the timeseries view keys.

    """

    # First, if the date key is 7 elements long, add three trailing
    # zeros to the millisecond string, effectively making it a
    # microsecond string.
    if len(key) == 7:
        key[6] += '000'

    # Construct a string of date components.
    dc = ''

    for i in range(0, len(key)):
        dc += str(int(key[i])) + ','

    # Now, try to create the actual datetime or date object.
    try:

        tmpl = '%Y-%m-%d'
        date = eval('datetime.datetime({})'.format(dc))

        if len(key) > 3:

            tmpl = '%Y-%m-%dT%H:%M:%S'

            if len(key) == 7:
                tmpl += '.%f'

            date = pytz.UTC.localize(date).astimezone(pytz.timezone(tz))

        else:
            date = date.date()

        if as_str == True:
            date = date.strftime(tmpl)

    except:
        date = None

    return date

