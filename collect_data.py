""" This module serves to collect data from the API. """
from dotenv import dotenv_values
import requests
import json
from time import sleep # TODO: something else for precision

def handle_json(resp_json: dict) -> None|list:
    """ There are 3 possibilities anticipated:
        - successful call to api, result is a list
        - result: "false", error: "...error message..."
        - result: "...error message..."

        Returns None if unsuccessful, list of data about vehicles if successful.
    """
    if 'result' not in resp_json:
        print("CRITICAL ERROR (contact devs): unexpected: no result field in response")
        # TODO: dump response to file to investigate
        return

    result = resp_json['result']

    if isinstance(result, list):
        print("SUCCESSFUL CALL TO API")
        return result

    if not isinstance(result, str):
        print("CRITICAL ERROR (contact devs): result neither a list nor a string")
        return

    # result is a string
    if result == "false":
        if 'error' in resp_json:
            print("ERROR:", resp_json['error'])
        else:
            print("CRITICAL ERROR (contact devs): unexpected: result = \false\", no error field")
        return
    # result is a string nad not a "false"
    print("ERROR in result:", result)

# TODO: typing.TextIO
# TODO?: somehow don't parse the json too much?
def dump(data_list: list, file) -> None:
    """ Dumps the data to a file as json lines.  """
    for data in data_list:
        file.write(json.dumps(data) + '\n')

config = dotenv_values(".env")
API_KEY = config["API_KEY"]
POSITION_API_URL = 'https://api.um.warszawa.pl/api/action/busestrams_get'
POSITION_API_RESOURCE_ID = 'f2e5503e927d-4ad3-9500-4ab9e55deb59'
BUS_TYPE = 1
TRAM_TYPE = 0

params = {
    'resource_id': POSITION_API_RESOURCE_ID,
    'apikey': API_KEY,
    'type': BUS_TYPE,
    # 'line':
    # 'brigade':
}


# TODO: preflight? (HEAD, check if there is new)
# no need if we get 10s right
# https://stackoverflow.com/questions/3393612/run-certain-code-every-n-seconds 
FILE_NAME = "data.jsonl"
with open(FILE_NAME, 'a') as file:
    for i in range(3):
        if i > 0:
            sleep(10) # TODO: threading or scheduling + coordinate with retries
        data_list: None = None # not the right type: make sure this screams and then fix
        while data_list is None:
            # TODO: handle failed timeout
            response = requests.get(url=POSITION_API_URL, params=params, timeout=5)
            j_response = response.json()
            data_list = handle_json(j_response)
            if data_list is None: # while true for clean break before sleep?
                # print("Fail, retrying...")
                sleep(1)

        # if data_list is not None:
        assert data_list is not None
        dump(data_list, file)


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