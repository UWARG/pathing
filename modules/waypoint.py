"""
Class to store LocationGround and corresponding altitude.
"""

import math

from .common.kml.modules import location_ground

# Earth radius in meters
EARTH_RADIUS = 6378137


class Waypoint:
    """
    LocationGroundAndAltitude represents a geographical ground location and an altitude
    with a name, latitude, longitude, and altitude.

    Attributes:
        name (str): The name or label for the location.
        latitude (float): The latitude coordinate in decimal degrees.
        longitude (float): The longitude coordinate in decimal degrees.
        altitude (float): The altitude coordinate in metres.

    Methods:
        __init__(name, latitude, longitude, altitude): Initializes a LocationGroundAndAltitude object.
        __eq__(other): Checks if two LocationGroundAndAltitude objects are equal.
        __repr__(): Returns a string representation of the LocationGroundAndAltitude object.
    """

    def __init__(self, name: str, latitude: float, longitude: float, altitude: float) -> None:
        """
        Constructor for the LocationGroundAndAltitude object.

        Args:
            name (str): The name or label for the location.
            latitude (float): The latitude coordinate in decimal degrees.
            longitude (float): The longitude coordinate in decimal degrees.
            altitude (float): The altitude of the coordinate in metres.
        """
        self.location_ground = location_ground.LocationGround(name, latitude, longitude)
        self.altitude = altitude

    def __eq__(self, other: "Waypoint") -> bool:
        """
        Checks if two LocationGroundAndAltitude objects are equal.

        Args:
            other (LocationGroundAndAltitude): The other LocationGroundAndAltitude object to compare to.
        """
        if not isinstance(other, Waypoint):
            return False

        return self.location_ground == other.location_ground and self.altitude == other.altitude

    def __repr__(self) -> str:
        """
        String representation
        """
        return f"LocationGroundAndAltitude: {str(self.location_ground)}, altitude: {self.altitude}"


def waypoint_distance(point_1: Waypoint, point_2: Waypoint) -> "tuple[bool, float]":
    """Return the great-circle distance of two points Earth, using Haversine's
    formula.

    Args:
        point_1 (Waypoint): First point
        point_2 (Waypoint): Second point

    Returns:
        tuple[bool, float]: Returns (False, 0) if the altitudes are different,
            and (True, distance) otherwise, where distance is the great-circle
            distance between point_1 and point_2.
    """
    # this function only calculates distance for waypoints with the same
    # altitude
    if point_1.altitude != point_2.altitude:
        return False, 0

    lat1, lon1, lat2, lon2 = map(
        math.radians,
        [
            point_1.location_ground.latitude,
            point_1.location_ground.longitude,
            point_2.location_ground.latitude,
            point_2.location_ground.longitude,
        ],
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # since the points have altitudes, the distance to the center of the earth
    # (the radius) is actually the Earth's radius plus the altitude
    radius = EARTH_RADIUS + point_1.altitude
    return True, c * radius
