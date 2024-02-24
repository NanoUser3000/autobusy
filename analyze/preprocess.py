import json
import argparse
import re
from lib.distance import MIN_LON, MIN_LAT, MAX_LON, MAX_LAT
### TODO: might turn out to be unnecessary

date_pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
# TODO: 2024? hm?

# TODO: docs
# assume each datum has
# - Lines
# - VehicleNumber
# - Time in format "2021-05-01 12:34:56"
# - Brigade
# - Lon (number)
# - Lat (number)
def transform_datum(datum: dict):
    """ Returns None for invalid data """
    if not re.match(date_pattern, datum['Time']):
        return None
    if not MIN_LAT < datum['Lat'] < MAX_LAT:
        return None
    if not MIN_LON < datum['Lon'] < MAX_LON:
        return None
    # datum['Time'] = datetime.strptime(datum['Time'], "%Y-%m-%d %H:%M:%S").timestamp()
    return datum

parser = argparse.ArgumentParser(description="Preprocesses the data.")
parser.add_argument('input', type=str, help='The input file.')
parser.add_argument('-o','--output', type=str, help='The output file. Defaults to preprocessed_<input>', required=False)
args = parser.parse_args()
if args.output is None:
    args.output = f"preprocessed_{args.input}"

# TODO: check that the output file does not exist, prompt or exit

with open(args.input, 'r') as input_f, open(args.output, 'w') as output_f:
    count = 0
    count_failed = 0
    for line in input_f:
        datum = json.loads(line)
        transformed = transform_datum(datum)
        if transformed is not None:
            output_f.write(json.dumps(transformed))
            output_f.write('\n')
        else:
            count_failed += 1
        count += 1

print(f"Removed {count_failed} out of {count} entries ({count_failed/count * 100}%).\n")