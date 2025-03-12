"""
Module to plot n circular waypoints, given a center and radius.
"""

import csv
import math
import pathlib

from modules.common.modules import position_global
from modules.common.modules import position_global_relative_altitude
from modules.common.modules import location_local
from modules.common.modules.mavlink import local_global_conversion


def move_coordinates_by_offset(
    start_point: position_global_relative_altitude.PositionGlobalRelativeAltitude,
    offset_x: float,
    offset_y: float,
) -> (
    tuple[bool, position_global_relative_altitude.PositionGlobalRelativeAltitude]
    | tuple[False, None]
):
    """
    Given a starting waypoint and offsets x and y displacements, find the
    resulting waypoint.

    starting_point: The starting waypoint.
    offset_x: Offset in west-east direction in metres. East is positive.
    offset_y: Offset in north-south direction in metres. North is positive.

    Return: Success, waypoint.
    """
    result, offset_local = location_local.LocationLocal.create(offset_y, offset_x)
    if not result:
        return False, None

    # Required for conversion input
    # TODO: Change when local_global_conversion is updated
    result, start_point_converted = position_global.PositionGlobal.create(
        start_point.latitude,
        start_point.longitude,
        0.0,
    )
    if not result:
        return False, None

    result, end_point = local_global_conversion.position_global_from_location_local(
        start_point_converted, offset_local
    )
    if not result:
        return False, None

    return position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
        end_point.latitude, end_point.longitude, start_point.relative_altitude
    )


def generate_circular_path(
    centre: position_global_relative_altitude.PositionGlobalRelativeAltitude,
    radius: float,
    num_points: int,
) -> (
    tuple[bool, list[position_global_relative_altitude.PositionGlobalRelativeAltitude]]
    | tuple[False, None]
):
    """
    Generate a list of `num_points` evenly-separated waypoints given a centre and radius.
    The first point is appended as an extra point at the end of the itinerary,
    so that the drone completes a full circle.

    centre: The centre of the circular path.
    radius: The length of the radius, in metres.
    num_points: The number of waypoints to generate.

    Return: Success, list of waypoints.
    """
    if radius <= 0.0:
        return False, None

    if num_points <= 0:
        return False, None

    waypoints = []

    # Any two consecutive points are separated by 2 * pi / n radians.
    for i in range(num_points):
        # Angle of rotation
        angle = 2 * math.pi / num_points * i
        offset_x = radius * math.cos(angle)
        offset_y = radius * math.sin(angle)

        result, waypoint = move_coordinates_by_offset(centre, offset_x, offset_y)
        if not result:
            return False, None

        waypoints.append(waypoint)

    # The drone should return back to the same point to complete a full circle
    waypoints.append(waypoints[0])

    return True, waypoints


def save_waypoints_to_csv(
    waypoints: list[position_global_relative_altitude.PositionGlobalRelativeAltitude],
    filepath: pathlib.Path,
) -> bool:
    """
    Save a list of waypoints to a CSV file.

    waypoints: The list of waypoints to save.
    filepath: The full path of the CSV file to save the waypoints to, including name.
    """

    try:
        with open(filepath, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Latitude", "Longitude", "Altitude"])
            for waypoint in waypoints:
                writer.writerow(
                    [
                        waypoint.latitude,
                        waypoint.longitude,
                        waypoint.relative_altitude,
                    ]
                )
        return True
    # Required for catching library exceptions
    # pylint: disable-next=broad-exception-caught
    except Exception as exception:
        print(f"Failed to write with exception: {exception}")

    return False
