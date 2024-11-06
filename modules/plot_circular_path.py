"""
Module to plot n circular waypoints, given a center and radius.
"""

import csv
import math

from modules.common.mavlink.modules.drone_odometry import DronePosition
from modules.common.mavlink.modules.drone_odometry_local import DronePositionLocal
from modules.common.mavlink.modules.local_global_conversion import drone_position_global_from_local

from .waypoint import Waypoint


def move_coordinates_by_offset(
    start_point: Waypoint, offset_x: float, offset_y: float, name: str
) -> "tuple[bool, Waypoint | None]":
    """Given a starting waypoint and offsets x and y displacements, find the
    resulting waypoint.

    Args:
        starting_point (Waypoint): The starting waypoint
        offset_x (float): The offset in the west-east direction. Positive for
            east, negative for west.
        offset_y (float): The offset in the north-south direction. Positive for
            north, negative for south.
        name (str): The name for the resulting waypoint

    Returns:
        tuple[bool, Waypoint | None]: Either return (False, None), indicating a
            a failure in execution, or (True, waypoint), where waypoint is the
            resulting waypoint.
    """
    success, offset_local = DronePositionLocal.create(offset_y, offset_x, 0)
    if not success:
        return False, None

    # Because drone_position_global_from_local requires DronePosition class,
    # we need to convert Waypoint to DronePosition first
    success, start_point_converted = DronePosition.create(
        start_point.location_ground.latitude,
        start_point.location_ground.longitude,
        start_point.altitude,
    )
    if not success:
        return False, None

    success, end_point = drone_position_global_from_local(start_point_converted, offset_local)
    if not success:
        return False, None

    return True, Waypoint(name, end_point.latitude, end_point.longitude, end_point.altitude)


def generate_circular_path(
    center: Waypoint, radius: float, num_points: int
) -> "tuple[bool, list[Waypoint] | None]":
    """Generate a list of `num_points` evenly-separated waypoints given a center
    and radius.

    Args:
        center (Waypoint): The center of the circular path
        radius (float): The length of the radius, in meters
        num_points (int): The number of waypoints to generate

    Returns:
        tuple[bool, list[Waypoint] | None]: Either return (False, None),
            indicating a failure in execution, or (True, waypoints), where
            waypoints is the list of waypoints forming a circle `radius` away
            from `center`.
    """
    # validate input
    if radius <= 0 or num_points <= 0:
        return False, None

    waypoints = []

    # any two consecutive points are separated by 2 * pi / n radians.
    for i in range(num_points):
        # number of radians away from standard position
        rad = 2 * math.pi / num_points * i
        offset_x = radius * math.cos(rad)
        offset_y = radius * math.sin(rad)

        success, waypoint = move_coordinates_by_offset(
            center, offset_x, offset_y, f"Waypoint {i + 1}"
        )
        if not success:
            return False, None

        waypoints.append(waypoint)

    return True, waypoints


def save_waypoints_to_csv(waypoints: "list[Waypoint]", filename: str) -> None:
    """Save a list of waypoints to a CSV file.

    Args:
        waypoints (list[Waypoint]): The list of waypoints to save
        filename (str): The name of the CSV file to save the waypoints to
    """

    with open(filename, mode="w", encoding="UTF-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Latitude", "Longitude", "Altitude"])
        for waypoint in waypoints:
            writer.writerow(
                [
                    waypoint.location_ground.name,
                    waypoint.location_ground.latitude,
                    waypoint.location_ground.longitude,
                    waypoint.altitude,
                ]
            )
