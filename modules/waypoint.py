
# Class waypoint to use instead of tuple for coordinates
class Waypoint:
    def __init__(self, name: str, latitude: float, longitude: float):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
    
    # Override __eq__ to compare Waypoint objects for testing
    def __eq__(self, other):
        if isinstance(other, Waypoint):
            return (self.name == other.name and
                    self.latitude == other.latitude and
                    self.longitude == other.longitude)
        return False