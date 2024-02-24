import json
import logging, logging.config

def configure_logging(filename: str) -> None:
    """ Configures logging using the provided json file. """
    with open(filename,'r') as f:
        logging_config = json.load(f)
    logging.config.dictConfig(config=logging_config)

def get_logger() -> logging.Logger:
    """ Returns the 'collect_data' logger. """
    return logging.getLogger('collect_data')

    # TODO: try what it does:
    # """ Returns the logger for the current module. """
    # return logging.getLogger(__name__) 