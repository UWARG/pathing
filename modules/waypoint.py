"""
Class Waypoint to use instead of tuple for coordinates.
""" 

class Waypoint:
    """
    Waypoint class represents a geographical waypoint with a name, latitude, and longitude.

    Attributes:
        name (str): The name or label for the waypoint.
        latitude (float): The latitude coordinate of the waypoint in decimal degrees.
        longitude (float): The longitude coordinate of the waypoint in decimal degrees.    
    """    
    def __init__(self, name: str, latitude: float, longitude: float):
        """
        Initializes a Waypoint object.

        Args:
            name (str): The name or label for the waypoint.
            latitude (float): The latitude coordinate of the waypoint in decimal degrees.
            longitude (float): The longitude coordinate of the waypoint in decimal degrees.

        """
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
    
    def __eq__(self, other):
        """
        Checks if two Waypoint objects are equal.
        """
        if isinstance(other, Waypoint):
            return (self.name == other.name and
                    self.latitude == other.latitude and
                    self.longitude == other.longitude)
        return False
    