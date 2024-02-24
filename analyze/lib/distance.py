""" Distance functions for locations on Earth."""
from math import radians, cos, sin, asin, sqrt

# (Lon, Lat)
Position = tuple[float, float]

MIN_LAT = 51.5
MAX_LAT = 53.5
MIN_LON = 20.5
MAX_LON = 21.5

# TODO: tests
# TODO: document limitations of these functions (esp. very close locations across the 180 line)
def earth_distance_km(p1: Position, p2: Position, earth_radius=6371) -> float:
    """ Returns distance in kilometers between two points on Earth.
    The points should be given as pairs (lon, lat)"""
    # radius of Earth in kilometers (6357-6378km)
    R = earth_radius
    # R = 6371

    lon1, lat1 = p1
    lon2, lat2 = p2

    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a)) # @improve: check if a isn't > 1 by floating point error
    return (c * R)

def warsaw_distance_km(p1: Position, p2: Position) -> float:
    """ Returns distance in kilometers between two points in Warsaw
    using Pythagoras'.
    The points should be given as pairs (lon, lat)"""
    warsaw_lat = 52.237049
    # warsaw_lon = 21.017532
    lon1, lat1 = p1
    lon2, lat2 = p2
    if not MIN_LAT < lat1 < MAX_LAT or not MIN_LAT < lat2 < MAX_LAT:
        raise ValueError("Latitude out of range of Warsaw")
    # note: the longitude doesn't matter much
    R = 6374.9 # earth radius in warsaw using https://rechneronline.de/earth-radius/

    # km per degree in both directions
    lat_degree_km = 111 # google/circumference of Earth vertically is 40,000 km
    tropic_radius = cos(radians(warsaw_lat)) * R
    lon_degree_km = tropic_radius * radians(1)

    lon_diff = (lon1 - lon2) * lon_degree_km
    lat_diff = (lat1 - lat2) * lat_degree_km
    dist = sqrt(lon_diff**2 + lat_diff**2)
    return dist

def warsaw_numbers() -> tuple[float, float]:
    """ Returns (km_per_degree_lon, km_per_degree_lat) for Warsaw."""
    warsaw_lat = 52.237049
    # warsaw_lon = 21.017532
    # note: the longitude doesn't matter much
    R = 6374.9 # earth radius in warsaw using https://rechneronline.de/earth-radius/

    # km per degree in both directions
    lat_degree_km = 111 # google/circumference of Earth vertically is 40,000 km
    tropic_radius = cos(radians(warsaw_lat)) * R
    lon_degree_km = tropic_radius * radians(1)
    return (lon_degree_km, lat_degree_km)

# TODO: tests
def main():
    # lat1 = 53.32055555555556
    # lat2 = 53.31861111111111
    # lon1 = -1.7297222222222221
    # lon2 = -1.6997222222222223
    lat1 = 52.32055555555556
    lat2 = 52.31861111111111
    lon1 = -1.7297222222222221
    lon2 = -1.6997222222222223
    p1 = (lon1,lat1)
    p2 = (lon2,lat2)
    e_default = earth_distance_km(p1,p2)
    e_6374_9 = earth_distance_km(p1,p2,earth_radius=6374.9)
    w = warsaw_distance_km(p1,p2)
    print('earth default    ', e_default, "km")
    print('earth with 6374.9', e_6374_9, "km")
    print('warsaw           ', w, "km")
    min = min(e_default, e_6374_9, w)
    assert min > 0
    max = max(e_default, e_6374_9, w)
    # less then 0.5% difference
    relative_error = abs(max-min)/min
    print('relative error', relative_error)
    assert relative_error < 0.5 * 0.01

if __name__ == "__main__":
    main()
