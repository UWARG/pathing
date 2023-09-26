

# Class waypoint to use instead of tuple for coordinates
class Waypoint:
    def __init__(self, name: str, latitude: float, longitude: float):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude