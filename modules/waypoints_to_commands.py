"""
Function to convert list of waypoints to dronekit commands.
"""

from . import generate_command
from .common.modules import location_global
from .common.modules import position_global_relative_altitude
from .common.modules.mavlink import flight_controller


ACCEPT_RADIUS = 5.0  # metres


def waypoints_to_commands(
    waypoints: list[location_global.LocationGlobal], altitude: float
) -> tuple[True, list[flight_controller.dronekit.Command]] | tuple[False, None]:
    """
    Convert list of waypoints to dronekit commands.

    waypoints: List of locations.
    altitude: Altitude above home in metres to command the drone to.

    Return: Success, dronekit commands that can be sent to the drone.
    """
    if len(waypoints) == 0:
        return False, None

    dronekit_command_list = []

    for waypoint in waypoints:
        command = generate_command.waypoint(
            0.0, ACCEPT_RADIUS, waypoint.latitude, waypoint.longitude, altitude
        )

        dronekit_command_list.append(command)

    return True, dronekit_command_list


def waypoints_with_altitude_to_commands(
    waypoints: list[position_global_relative_altitude.PositionGlobalRelativeAltitude],
) -> tuple[True, list[flight_controller.dronekit.Command]] | tuple[False, None]:
    """
    Convert list of waypoints to dronekit commands.

    waypoints: List of positions.

    Return: Success, dronekit commands that can be sent to the drone.
    """
    if len(waypoints) == 0:
        return False, None

    dronekit_command_list = []

    for waypoint in waypoints:
        command = generate_command.waypoint(
            0.0,
            ACCEPT_RADIUS,
            waypoint.latitude,
            waypoint.longitude,
            waypoint.relative_altitude,
        )

        dronekit_command_list.append(command)

    return True, dronekit_command_list
