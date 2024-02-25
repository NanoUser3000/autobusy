""" Module for getting info about schedules.
    From downloads and from dbtimetable_get.
"""
import json
# .download is not used as it is not good with jupyter notebooks
# this works for both script and jupyter
from analyze.downloads.download import DICTIONARY_FILE, STOPS_FILE, ROUTES_FILE, ENCODING

def values_to_dict(stop):
    """ Transform list of {key:...,value:...} objects into a dictionary. """
    ret = {}
    for pair in stop['values']:
        ret[pair['key']] = pair['value']
    return ret

def _load_json_result(file):
    """ From a json file with only key 'result', get its value. """
    with open(file, 'r', encoding=ENCODING) as f:
        jraw = json.load(f)
        # smalltodo: dict_keys(['result']) by hand? learn
        if not isinstance(jraw, dict):
            raise RuntimeError(f"In file {file} json is not an object.")
        keys = jraw.keys()
        expected_keys = {'result':''}.keys()
        if keys != expected_keys:
            raise RuntimeError(f"In file {file} the are keys {keys}, not expected {expected_keys}")
        return jraw['result']

# _raw as in not processed, as downloaded
# although we peeled value from the 'result' key
try:
    dictionary_raw = _load_json_result(DICTIONARY_FILE)
    stops_raw = _load_json_result(STOPS_FILE)
    routes_raw = _load_json_result(ROUTES_FILE)
except FileNotFoundError as e:
    print(f"File not found: {e.filename}")
    print("Download the files!")
    raise e

DICTIONARY = dictionary_raw
STOPS = list(map(values_to_dict, stops_raw))
ROUTES = routes_raw

################################################################################
# db_timetable_get stuff
################################################################################