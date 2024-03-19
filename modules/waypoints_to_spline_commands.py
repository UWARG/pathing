"""
Function to convert list of waypoints a list of spline waypoint dronekit commands.
"""

import dronekit

from .common.kml.modules import location_ground


MAVLINK_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_SPLINE_WAYPOINT


def waypoints_to_spline_commands(waypoints: "list[location_ground.LocationGround]",
                                 altitude: int) -> "tuple[bool, list[dronekit.Command] | None]":
    """
    Convert list of waypoints to a list of spline waypoint dronekit commands.
    Spline waypoint dronekit commands fly to the target waypoint following a spline path(a path that curves around a waypoint) then hover in place.

    Parameters
    ----------
    waypoints: list[LocationGround]
        list of locationGround objects containing names and coordinates in decimal degrees.
    altitude: int
        altitude in meters to command the drone to.

    Returns
    -------
    tuple[bool, list[dronekit.Command] | None]: 
        (False, None) if empty waypoints list,
        (True, list of spline waypoint commands) otherwise spline waypoint dronekit commands that can be sent to the drone.
    """
    if len(waypoints) == 0:
        return False, None

    dronekit_spline_command_list = []

    for waypoint in waypoints:
        command = dronekit.Command(
            0,
            0,
            0,
            MAVLINK_FRAME,
            MAVLINK_COMMAND,
            0,
            0,
            0,  # param1
            0,
            0,
            0,
            waypoint.latitude,
            waypoint.longitude,
            altitude,
        )
        dronekit_spline_command_list.append(command)

    return True, dronekit_spline_command_list
