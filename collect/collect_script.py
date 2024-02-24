""" This module serves to collect data from the API. """
import requests
import json
from time import sleep
from lib.utils import * # TODO: import lib.utils (as...?)
from lib.loggers import get_logger

logger = get_logger('collect_data')

# TODO: info about params
logger.info("Starting the program")

def create_extra(resp_json):
    """ Helper to create details for logging. """
    return {
        'details': "The response json received:\n"
                   + json.dumps(resp_json, indent=4),
    }

def handle_json(resp_json: dict) -> None|list:
    # TODO: what does this do though
    """ Handles the json response from the API:
    - if the request was successful, returns the data
     (a list of dictionaries with data about vehicle positions)
    - if it was unsuccessful, logs the error and returns None.

    There are 2 possibilities anticipated:
        - successful call to api, value under "result" key is a list
        - result: "false", error: "...error message..."
    Other cases are logged with level error or higher.

    Returns None if unsuccessful, list of data about vehicles if successful.
    """
    if 'result' not in resp_json:
        logger.critical('Unexpected: no result field in response',
                     extra=create_extra(resp_json))
        return None

    result = resp_json['result']

    if isinstance(result, list):
        # SUCCESS!
        return result

    if not isinstance(result, str):
        logger.critical('Unexpected: result neither a list nor a string',
                     extra=create_extra(resp_json))
        return None

    assert isinstance(result, str)

    if result == "false" and 'error' in resp_json:
        # note: this happens, we don't really know why # TODO ?
        logger.warning('API call failed with error message: \"%s\"',
                        resp_json['error'])
    elif result == "false":
        logger.error('Unexpected (but not breaking):'
                     + ' result \"false\", no error message',
                     extra=create_extra(resp_json))
    else:
        logger.warning('API call failed with result \"%s\"', result)
    return None
    
# TODO: typing.TextIO
def dump(data_list: list, file) -> None:
    """ Dumps the data to a file as json lines.  """
    for data in data_list:
        file.write(json.dumps(data) + '\n')
    return None

POSITION_API_URL = 'https://api.um.warszawa.pl/api/action/busestrams_get'
POSITION_API_RESOURCE_ID = 'f2e5503e-927d-4ad3-9500-4ab9e55deb59'

BUS_TYPE = 1
TRAM_TYPE = 0

params = {
    'resource_id': POSITION_API_RESOURCE_ID,
    'apikey': get_api_key(),
    'type': BUS_TYPE,
    # 'line': 0,
    # 'brigade':
}

SECOND = 1
HOUR = 3600 * SECOND

# generate filename based date and time
# ! OLD: FILE_NAME = "data/data.jsonl"
dt_string = get_current_datetime_for_filename()
FILE_NAME = f"data/{dt_string}_data.jsonl"

# minimum interval after successful request (measure from the beginning to beginning)
SUCC_INTERVAL = 10 * SECOND
# minimum wait time after failed request (measure from the end to beginning)
MIN_INTERVAL = 2 * SECOND

def get_data_list():
    """ Sends a request to API. Returns the list of vehicle positions from the API or None if unsuccessful."""
    # maybe post with params in body is worth a try? nah # TODO cleanup
    response = requests.get(url=POSITION_API_URL, params=params, timeout=8)
    json_response = response.json()
    return handle_json(json_response)


# TODO: provided by user or something
COLLECTION_TIME = 3*HOUR

from normal.collect.lib.utils import get_time
now = get_time()
END = now + COLLECTION_TIME
last_try = now - 2 * MIN_INTERVAL # long time ago

logger.info("Starting to collect data for %d hours", COLLECTION_TIME/HOUR)

success_count = 0
failure_count = 0
MOD = 50 # how often to log above counts

with open(FILE_NAME, 'a') as file:
    file.write(f"# Data collected every {SUCC_INTERVAL} seconds,"
               f" wait {MIN_INTERVAL} after failure\n")
    while (now := get_time()) < END:
        since_last_try = now - last_try
        if since_last_try < MIN_INTERVAL:
            sleep(MIN_INTERVAL - since_last_try)
        before_req = get_time()
        logger.info("Sending request to the API")
        data_list = get_data_list()
        last_try = get_time()
        if data_list is not None:
            # last_succ = before_req
            dump(data_list, file)
            logger.info("Dumped %d position records successfully", len(data_list))
            since_last_succ = get_time() - before_req
            # sleep after success that just happenned
            if since_last_succ < SUCC_INTERVAL:
                sleep(SUCC_INTERVAL - since_last_succ)
        if data_list is None:
            failure_count += 1
        else:
            success_count += 1
        if (success_count + failure_count) % MOD == 0:
            logger.debug("Total of %d successful requests and %d failed requests so far",
                        success_count, failure_count)


### ideas for analyzing data
# sort by vehicle number, then by time
# little exercise style
# discard data about speed if the time difference is too big (configurable? but for analyzing!)
# analyze the time data (long breaks) # may be a problem with the "loop", or maybe not -- see if can identify "loops" (long stops) via this or long not moving
# maybe that's the interpretation for long breaks in data with similar position, or breaks in movement

# Configurable: longitude and latitude of the city
# something funny like request to get it from the internet

# TODO: need to calculate distance in lon lat coordinates

# TODO: validate the keys we are interested in (that they're there) + what is allowed (?)
