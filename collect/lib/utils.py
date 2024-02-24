from datetime import datetime
from dotenv import dotenv_values
import json
import logging, logging.config

def get_time() -> float:
    """ Returns the current time in seconds since 1970. """
    return datetime.now().timestamp()

def get_api_key() -> str:
    """ Returns the API key from the .env file."""
    config = dotenv_values(".env")
    # TODO cleanup
    # config = dotenv_values("C:\\Users\\user\\Documents\\3 rok\\pyton\\autobusy\\normal\\collect\\.env")
    API_KEY = config["API_KEY"]
    return API_KEY

def get_current_datetime_for_filename() -> str:
    """ Returns the current date and time in the format
    suitable for a file name. """
    return datetime.now().strftime("%Y_%m_%d_%H%M%S")

def split_dict(d: dict, keys1: list) -> tuple[dict, dict]:
    """ Splits the dictionary into one with keys from the list and one with the rest.
    Input dictionary may not have all the keys from the list.
    """
    d1 = {k: v for k, v in d.items() if k in keys1}
    d2 = {k: v for k, v in d.items() if k not in keys1}
    return d1, d2