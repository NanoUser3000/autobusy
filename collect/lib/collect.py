from .loggers import get_logger
from .constants import POSITION_API_URL, POSITION_API_RESOURCE_ID
from .utils import get_time, get_api_key
from time import sleep

import json
import requests

# TODO: think about:
# 1. logger: could define those functions inside of the other one but...
#    or just call get_logger() all over the place
#    . pass the logger in the main function if we pass it inside?
# 2. _visibility (the only function exported should be collect_data)
# 3. maybe do utils?

def complete_params(params: dict) -> dict:
    params = params.copy()
    params['resource_id'] = POSITION_API_RESOURCE_ID
    params['apikey'] = get_api_key()
    return params

# TODO: typing.TextIO
def dump(data_list: list, file) -> None:
    """ Dumps the data to a file as json lines. """
    for datum in data_list:
        file.write(json.dumps(datum) + '\n')
    return None

def _create_extra(resp_dict: dict) -> dict:
    """ Helper to create details for logging. """
    return {
        'details': "The response json received:\n"
                   + json.dumps(resp_dict, indent=4),
    }

# TODO type logger
def handle_json_response(resp_dict: dict, logger) -> None|list:
    """ Handles the json response from the API:
    - if the request was successful, returns the data
     (a list of dictionaries with data about vehicle positions)
    - if it was unsuccessful, logs the error and returns None.

    There are 3 possibilities anticipated:
        - successful call to api, value under "result" key is a list
        - result: "false", error: "...error message..."
        - result: "...error message..."
    Other cases are logged with level error or higher.

    Returns None if unsuccessful, list of data about vehicles if successful.
    """
    if 'result' not in resp_dict:
        logger.critical('Unexpected: no result field in response',
                     extra=_create_extra(resp_dict))
        return None

    result = resp_dict['result']

    if isinstance(result, list):
        # SUCCESS!
        return result

    if not isinstance(result, str):
        logger.critical('Unexpected: result neither a list nor a string',
                     extra=_create_extra(resp_dict))
        return None

    assert isinstance(result, str)

    if result == "false" and 'error' in resp_dict:
        # note: this happens, we don't really know why # TODO ?
        logger.warning('API call failed with error message: \"%s\"',
                        resp_dict['error'])
    elif result == "false":
        logger.error('Unexpected (but not breaking):'
                     + ' result \"false\", no error message',
                     extra=_create_extra(resp_dict))
    else:
        logger.warning('API call failed with result \"%s\"', result)
    return None

def get_data_list(params: dict, logger, timeout: float) -> None|list:
    """ Sends a request to the API.  Returns the list of vehicle positions
    from the API or None (if unsuccessful).
    TODO: complete doc?
    """
    response = requests.get(url=POSITION_API_URL, params=params, timeout=timeout)
    try:
        json_response = response.json()
    except requests.Requests.JSONDecodeError as e:
        logger.error("Failed to decode the API response as json", exc_info=False, extra={'details': f'response:\n{response.text}'})
        return None
    return handle_json_response(json_response, logger)

def collect_data(*, duration: float, filename: str, params: dict,
                 success_interval: int, min_interval: int,
                 log_frequency: int = 50) -> None:
    """ Collects data about vehicles in Warsaw for the given duration.
    Saves the data to the given filename (append if exists).
    TODO: rest of parameters
    """
    logger = get_logger() # pass it as a parameter? whatever TODO cleanup

    censored_params = params
    params = complete_params(params)

    now = get_time()
    end = now + duration

    last_try = now - 2*min_interval # long time ago

    success_count = 0
    failure_count = 0

    req_timeout = success_interval - 1
    with open(filename, 'a') as file: 
        logger.info("Starting to collect data for %d hours into %s\n"
                    "Parameters: %s", duration/3600, filename, censored_params)
        while (now := get_time()) < end:
            since_last_try = now - last_try
            if since_last_try < min_interval:
                sleep(min_interval - since_last_try)
            before_req = get_time()
            logger.info("Sending request to the API")
            data_list = get_data_list(params, logger, req_timeout)
            last_try = get_time()
            if data_list is not None:
                dump(data_list, file)
                logger.info("Dumped %d position records successfully", len(data_list))
                since_last_succ = get_time() - before_req
                # sleep after success that just happenned
                if since_last_succ < success_interval:
                    sleep(success_interval - since_last_succ)
            if data_list is None:
                failure_count += 1
            else:
                success_count += 1
            if (success_count + failure_count) % log_frequency == 0:
                logger.debug("Total of %d successful requests and %d failed requests so far",
                             success_count, failure_count)

