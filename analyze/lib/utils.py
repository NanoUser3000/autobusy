""" Utils for analyzing data. """
import pandas as pd
# import numpy as np
# import json
from analyze.lib.distance import earth_distance_km, warsaw_distance_km

# TODO: problem: bus sends the same coords a few times, then new coords that place it at 120 km/h for a moment

def print_neighbours(df, idx, count=5):
    """ Print neighbours of the given index in the DataFrame.
    Assumes indexes are consecutive numbers.
    Count: count of neighbours to print on each side (so 2*count will be printed).
    """
    start_idx = max(idx - count, 0)
    end_idx = min(idx + count + 1, len(df))
    print(f"Neighbours of {idx} from {start_idx} to {end_idx-1}")
    for i in range(start_idx, end_idx):
        print("Neighbor", i)
        print(df.iloc[i])

# def df_from_jsonl(filename: str, columns: list) -> pd.DataFrame:
#     """ Reads a file in jsonl format and returns a DataFrame. """
#     data = []
#     with open(filename, 'r') as file:
#         for line in file:
#             try:
#                 data.append(json.loads(line))
#             except json.JSONDecodeError as e:
#                 print(f"Failed to decode the line as json: {line}")
#                 print('"',line,'"')
#                 print(e)
#                 exit(1)
#     return pd.DataFrame(data, columns=columns)
def df_from_jsonl(filename: str) -> pd.DataFrame:
    """ Reads a file in jsonl format and returns a DataFrame. """
    df = pd.read_json(filename, lines=True)
    # df = pd.read_json(filename, lines=True, convert_dates=['Time'], date_unit='s')
    df['Time'] = pd.to_datetime(df['Time'], format='ISO8601') # TODO: why the above doesn't work?
    return df
    ### df = df[df['Time'].astype(str).str.startswith('2024-')]

# KEYS = ['Lines', 'VehicleNumber', 'Time', 'Brigade', 'Lon', 'Lat']

def main():
    """ Example of analyzing data """
    # FILENAME = 'C:\\Users\\user\\Documents\\3 rok\\pyton\\autobusy\\normal\\analyze\\...'
    BIGFILE = '1data.jsonl'
    SMALLFILE = 'data.jsonl'

    # REALFILE = '../collect/data/2024_02_22_092914_data.jsonl'
    REALFILE = 'pre_bigdata'

    df = df_from_jsonl(REALFILE)
    # asdf = df.groupby('VehicleNumber')
    # could: discard vehicles with too few entries

    # TODO: df.drop_duplicates(subset=['VehicleNumber', 'Time'])
    # TODO first though: test with duplicates
    df.sort_values(by=['VehicleNumber', 'Time'], ascending=[True, True], inplace=True, ignore_index=True)

    # whatever, for now
    df.drop_duplicates(['VehicleNumber', 'Time'], inplace=True)

    # df_prev = df.copy()
    df_prev = df.shift(1)
    result = df.merge(df_prev, how='outer', left_index=True, right_index=True, suffixes=('', '_prev'))

    result = result[(result['VehicleNumber'] == result['VehicleNumber_prev'])
                    & (result['Time'] != result['Time_prev'])]
    # TODO: cleanup
    # for idx, row in result.iterrows():
    #     drop_cond = row['VehicleNumber'] != row['VehicleNumber_prev'] or row['Time'] == row['Time_prev']
    #     if drop_cond:
    #         result.drop(idx, inplace=True)

    result.drop(columns=['VehicleNumber_prev'], inplace=True)

    result['Dist_haversine'] = result.apply(lambda row: earth_distance_km((row['Lon'], row['Lat']), (row['Lon_prev'], row['Lat_prev'])), axis=1)
    # this should go nicely manually (np if needed)
    result['Dist_pythagoras'] = result.apply(lambda row: warsaw_distance_km((row['Lon'], row['Lat']), (row['Lon_prev'], row['Lat_prev'])), axis=1)
    result['Time_diff'] = (result['Time'] - result['Time_prev']).dt.total_seconds()
    # TODO!!!
    # filter out too big time diffs
    result['velocity_h'] = result['Dist_haversine'] / result['Time_diff'] * 3600
    result['velocity_p'] = (result['Dist_pythagoras'] / result['Time_diff']) * 3600

    count = len(result)
    result = result[result['velocity_p'] < 120]
    count2 = len(result)
    print(f"Removed {count - count2} out of {count} entries ({(count - count2)/count * 100}%).\n(Too fast -- over 120 km/h)")

    ################################################################################
    # no removing below
    ################################################################################
    result.reset_index(inplace=True, drop=True)

    print(result.columns)
    # print(result[['Dist_pythagoras', 'Time_diff', 'velocity_p']])
    # print(result[['Dist_haversine', 'Time_diff', 'velocity_h']])

    result['relative_diff'] = abs(result['Dist_haversine'] - result['Dist_pythagoras']) / result['Dist_haversine']
    index_max = result['relative_diff'].idxmax()
    print("Max relative difference between haversine and pythagoras: ", result.loc[index_max]['relative_diff'])
    print("The rest:")
    print(result.loc[index_max])

    index_velo_max = result['velocity_p'].idxmax()
    print("Max velocity:", result.loc[index_velo_max]['velocity_p'])
    print("The rest:")
    print(result.loc[index_velo_max])
    print("Neighbours:")
    print_neighbours(result, index_velo_max)


    print()
    print(result['velocity_p'].describe())
    print()
    print(result['velocity_h'].describe())
    print()
    print(result['Time'].describe())
    print()
    print(result['Time_diff'].describe())


    # result = pd.concat([df, df_prev], axis=1)

if __name__ == "__main__":
    main()
