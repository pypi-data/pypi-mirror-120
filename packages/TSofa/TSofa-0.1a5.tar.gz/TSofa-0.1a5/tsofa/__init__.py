# Standard library imports.
import importlib
from types import ModuleType as _mt

# Local package imports.
from tsofa._views._base_d_rpt import Command as _D_RPT


# Define the allowable time resolutions of data in indexed by the
# Javascript views.
RESOLUTIONS = ('day', 'sec', 'mls',)


# Define the data function for retrieving data documents using the
# source ID value.
def _d_doc(res, db, params):

    data = None

    if res in RESOLUTIONS:

        _m = importlib.import_module('tsofa._views._d_doc_' + res)
        data = _m.Command().handle(**{'db': db, 'params': params})

    return data


# Define the data function for retrieving report objects using the
# source and report ID values.
def _d_rpt(res, db, params):

    data = None

    if res in RESOLUTIONS:

        _m = importlib.import_module('tsofa._views._d_rpt_' + res)
        data = _m.Command().handle(**{'db': db, 'params': params})

    return data


# Define the data function for retrieving values using the source,
# report, and element ID values.
def _d_elm(res, db, params):

    data = None

    if res in RESOLUTIONS:

        _m = importlib.import_module('tsofa._views._d_elm_' + res)
        data = _m.Command().handle(**{'db': db, 'params': params})

    return data


# Define a dynamic module for retrieving data.
data = _mt('data')
data.docs = _d_doc
data.elms = _d_elm
data.rpts = _d_rpt

# Set the summarize method for the data report views.
data.rpts.summarize = _D_RPT.summarize


# Define the function for retrieving source attribute information
# using the source and attribute ID values.
def _s_atr(res, db, params):

    attrs = None

    if res in RESOLUTIONS:

        _m = importlib.import_module('tsofa._views._s_atr_' + res)
        attrs = _m.Command().handle(**{'db': db, 'params': params})

    return attrs


# Define a dynamic module for retrieving source attribute information.
src = _mt('src')
src.atrs = _s_atr

