from lib.loggers import configure_logging, get_logger
from lib.constants import *
from lib.argparsing import ArgParser
from lib.collect import collect_data

configure_logging('log_config.json')
logger = get_logger()

parser = ArgParser(
    prog='collect/script.py',
    description='Collect data about vehicles in Warsaw.')
parsed = parser.parse_args()

duration = parsed['duration']
output_filename = parsed['output']
params = parsed['params']

# constants, could be made configurable
SUCCESS_INTERVAL = 10 # SUCCESS_INTERVAL seconds between successful request and next one
MIN_INTERVAL = 3 # next request minimum MIN_INTERVAL seconds after the previous one

# TODO!!! if file exists, ask if they are certain to append
try:
    collect_data(duration=duration,
            filename=output_filename,
            params=params,
            success_interval=10,
            min_interval=2,
    )
except KeyboardInterrupt:
    pass # TODO log info, print exiting after ki to stderr
except Exception as e:
    logger.error(e, exc_info=True, extra={'details': 'none'})
    # message = f"An exception occurred while collecting data: {type(e).__name__}"
    # extra = {'details': f"{e}"} # e.__repr__()
    # logger.error("An error occurred while collecting data.", extra=extra)
    raise e