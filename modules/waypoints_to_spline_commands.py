"""
Function to convert list of waypoints a list of spline waypoint dronekit commands.
"""

from . import generate_command
from .common.modules import location_global
from .common.modules.mavlink import flight_controller


def waypoints_to_spline_commands(
    waypoints: list[location_global.LocationGlobal], altitude: float
) -> tuple[True, list[flight_controller.dronekit.Command]] | tuple[False, None]:
    """
    Convert list of waypoints to a list of spline waypoint dronekit commands.
    Spline waypoint dronekit commands fly to the target waypoint following a spline path
    (a path that curves around a waypoint).

    waypoints: List of locations.
    altitude: Altitude in metres above home to command the drone to.

    Return: Success, list of spline waypoint commands.
    """
    if len(waypoints) == 0:
        return False, None

    dronekit_spline_command_list = []

    for waypoint in waypoints:
        command = generate_command.waypoint_spline(
            0.0, waypoint.latitude, waypoint.longitude, altitude
        )
        dronekit_spline_command_list.append(command)

    return True, dronekit_spline_command_list
