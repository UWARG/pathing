from modules import waypoint
from modules import load_waypoint_name_to_coordinates_map
import math
import pathlib


class Route:
    def __init__(
        self,
        route_number: int,
        passengers: int,
        start_waypoint: waypoint.location_ground.LocationGround,
        end_waypoint: waypoint.location_ground.LocationGround,
        max_weight: float,
        notes: str,
        profit: int,
    ):
        WAYPOINT_FILE_PATH = pathlib.Path("waypoints", "wrestrc_waypoints.csv")
        RESULT, WAYPOINT_NAMES_TO_COORDINATES = (
            load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
                WAYPOINT_FILE_PATH
            )
        )
        self.route_number = route_number
        self.passengers = passengers
        self.start_waypoint = WAYPOINT_NAMES_TO_COORDINATES[
            start_waypoint
        ]  # object that contains name and coordinates
        self.end_waypoint = WAYPOINT_NAMES_TO_COORDINATES[end_waypoint]
        self.max_weight = max_weight
        self.notes = notes
        self.profit = profit
        self.distance = self.distance_between_locations(self.start_waypoint, self.end_waypoint)

    def __str__(self):
        return f"Route {self.route_number}: {self.passengers} passengers, {self.max_weight} kg limit, from {self.start_waypoint} to {self.end_waypoint}, {self.profit}$ profit, distance {self.distance}m"

    @staticmethod
    def distance_between_locations(
        coordinate_1: waypoint.location_ground.LocationGround,
        coordinate_2: waypoint.location_ground.LocationGround,
    ) -> float:
        # get distance between coordinates in m

        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(
            math.radians,
            [
                coordinate_1.longitude,
                coordinate_1.latitude,
                coordinate_2.longitude,
                coordinate_2.latitude,
            ],
        )

        long_difference = lon2 - lon1
        lat_difference = lat2 - lat1

        dist = (
            2
            * 6371  # earth radius in km
            * math.asin(
                math.sqrt(
                    math.sin(lat_difference / 2) ** 2
                    + math.cos(lat1) * math.cos(lat2) * math.sin(long_difference / 2) ** 2
                )
            )
            * 1000
        )

        return dist
