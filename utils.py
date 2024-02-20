from math import radians, cos, sin, asin, sqrt

""" (Lon, Lat) """
type Position = tuple[float, float]

# TODO: tests
def earth_distance_km(p1: Position, p2: Position) -> float:
    """ Returns distance in kilometers between two points on Earth.
    The points should be given as pairs (lon, lat)"""
    # radius of Earth in kilometers (6357-6378km)
    R = 6371

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

# TODO: tests
if __name__ == "__main__":
    lat1 = 53.32055555555556
    lat2 = 53.31861111111111
    lon1 = -1.7297222222222221
    lon2 = -1.6997222222222223
    p1 = (lon1,lat1)
    p2 = (lon2,lat2)
    print(earth_distance_km(p1,p2), "km")
