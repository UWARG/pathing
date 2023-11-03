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
    
    Methods:
        __init__(name, latitude, longitude): Initializes a Waypoint object.
        __eq__(other): Checks if two Waypoint objects are equal.
        __repr__(): Returns a string representation of the Waypoint object.
    """    

    def __init__(self, name: str, latitude: float, longitude: float):
        """
        Constructor for the Waypoint object.

        Args:
            name (str): The name or label for the waypoint.
            latitude (float): The latitude coordinate of the waypoint in decimal degrees.
            longitude (float): The longitude coordinate of the waypoint in decimal degrees.
        """

        self.name = name
        self.latitude = latitude
        self.longitude = longitude
    
    def __eq__(self, other: "Waypoint"):
        """
        Checks if two Waypoint objects are equal.

        Args:
            other (Waypoint): The other Waypoint object to compare to.
        """

        if not isinstance(other, Waypoint):
            return False
        
        return (self.name == other.name 
                and self.latitude == other.latitude 
                and self.longitude == other.longitude)    

    def __repr__(self):
        """
        Returns a string representation of the Waypoint object.
        """

        return f"Waypoint name: {self.name}, latitude: {self.latitude}, longitude: {self.longitude})"
