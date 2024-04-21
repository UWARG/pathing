"""
Class to store LocationGround and corresponding altitude.
"""

from .common.kml.modules import location_ground


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
        return f"LocationGroundAndAltitude: {repr(self.location_ground)}, altitude: {self.altitude}"
