""" Script for downloading info about schedules. """
import os
import json
from time import sleep

import requests
from dotenv import dotenv_values

# for file writing, but also reading elsewhere (should be synchronized)
ENCODING = 'utf-8'

current_dir = os.path.dirname(__file__)

def get_path_root(relpath):
    """ Locate file relative to the root of the project. """
    path = os.path.join(current_dir, '../../', relpath)
    return os.path.normpath(path)
def get_path_dwn(dwnpath):
    """ Locate file in downloads directory (analyze/downloads/). """
    path = os.path.join(get_path_root('analyze/downloads/'), dwnpath)
    return os.path.normpath(path)

API_KEY = dotenv_values(get_path_root("collect/.env"))["API_KEY"]

DICTIONARY_FILE = get_path_dwn('dictionary.txt')
STOPS_FILE = get_path_dwn('stop_info.txt')
ROUTES_FILE = get_path_dwn('transport_routes.txt')

DICTIONARY_STUFF = {
    'url': 'https://api.um.warszawa.pl/api/action/public_transport_dictionary/',
    'params': {
        'apikey' : API_KEY,
    },
    'ofile' : DICTIONARY_FILE,
}
STOPS_STUFF = {
    'url': 'https://api.um.warszawa.pl/api/action/dbstore_get/',
    'params': {
        'apikey': API_KEY,
        'id': 'ab75c33d-3a26-4342-b36a-6e5fef0a3ac3',
    },
    'ofile': STOPS_FILE,
}
ROUTES_STUFF = {
    'url': 'https://api.um.warszawa.pl/api/action/public_transport_routes/',
    'params':{
        'apikey' : API_KEY,
    },
    'ofile' : ROUTES_FILE,
}

def download(stuff: dict) -> None:
    """ Download data from the api and save it to a file. """
    response = requests.get(url=stuff['url'], params=stuff['params'], timeout=20)
    # utf-8 probably doesn't hurt, but doesn't help either
    # smalltodo: how to encode in utf8 properly
    with open(stuff['ofile'], 'w', encoding=ENCODING) as file:
        file.write(json.dumps(response.json(), indent=4))

def get_already_existing(stuff_list: list) -> list:
    """ Return output files which already exists. """
    ret = []
    for stuff in stuff_list:
        file = stuff['ofile']
        if os.path.exists(file):
            ret.append(file)
    return ret

def main():
    """ Download some info about schedules, stops etc. """
    dwn_items = [DICTIONARY_STUFF, STOPS_STUFF, ROUTES_STUFF]
    # check which exist, error if any (for now?)
    existing = get_already_existing(dwn_items)
    if len(existing) > 0:
        # smalltodo: FileExistsError?
        raise RuntimeError("Some downloads already existed:\n"
                           + json.dumps(existing, indent=4))
    # download # sleep to not anger the server
    print('Wait...')
    sleep(10)
    for stuff in dwn_items:
        print(f"Downloading into {stuff['ofile']}")
        download(stuff)
        sleep(10)
    print()
    print('Success!')

if __name__ == '__main__':
    main()
