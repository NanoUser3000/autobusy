import argparse
from .constants import BUS_TYPE, TRAM_TYPE
from .utils import split_dict, get_current_datetime_for_filename

# how are they parsed
VEHICLE_TYPES = {
    "bus": BUS_TYPE,
    "b": BUS_TYPE,
    "tram": TRAM_TYPE,
    "t": TRAM_TYPE,
}

class ArgParser():
    """ What should be put in params """
    __KEYS_TO_PARAMS = ['type', 'line', 'brigade']

    def __init__(self, *args, **kwargs):
        """ TODO... parameters are passed in creating argparse
        Consider adding prog, description
        """
        self.parser = argparse.ArgumentParser(*args, **kwargs)
        ArgParser.__add_arguments(self.parser)

    def parse_args(self):
        """ Returns parsed arguments: params (present values ready to be sent),
                                    duration (in seconds), output
        """
        parsed = self.parser.parse_args()
        return ArgParser.__transform_parsed(parsed)

    @classmethod
    def __transform_parsed(cls, parsed):
        parsed = vars(parsed) # turn into a dict
        if parsed['output'] is None:
            parsed['output'] = f"data/{get_current_datetime_for_filename()}_data.jsonl"
        parsed = {k: v for k, v in parsed.items() if v is not None}

        parsed['type'] = VEHICLE_TYPES[parsed['type']]
        parsed['duration'] *= 3600

        params, rest = split_dict(parsed, ArgParser.__KEYS_TO_PARAMS)
        rest['params'] = params
        return rest

    @classmethod
    def __add_arguments(cls, parser: argparse.ArgumentParser) -> None:
        # what to collect data about
        parser.add_argument(
            '-t', '--type',
            choices=VEHICLE_TYPES.keys(),
            help='Type of vehicles to collect data about.',
            required=False,
            default='bus')

        parser.add_argument(
            '-l', '--line',
            help='Line number to collect data about.',
            required=False)

        parser.add_argument(
            '-b', '--brigade',
            help='Brigade number to collect data about.',
            required=False)

        # how long to collect data
        parser.add_argument(
            '-d', '--duration',
            help='Duration of the data collection in hours.',
            required=True,
            type=float
        )

        # where to save the data
        parser.add_argument(
            '-o', '--output',
            help='Where to save the data. Defaults to data/<timestamp>_data.jsonl.',
            required=False,
        )
        return None
# TODO: help mention default (always)
