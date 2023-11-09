"""
Function to convert list of waypoints to dronekit commands
"""
import dronekit

from . import waypoint


MAVLINK_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
ACCEPT_RADIUS = 10


def waypoints_to_commands(waypoints: "list[waypoint.Waypoint]",
                          altitude: int) -> "list[dronekit.Command]":
    """
    Convert list of waypoints to dronekit commands.

    Parameters
    ----------
    waypoints: list[Waypoint]
        list of Waypoint objects containing names and coordinates in decimal degrees.
    altitude: int
        altitude in meters to command the drone to.

    Returns
    -------
    list[dronekit.Command]
        dronekit commands that can be sent to the drone.
    """
    dronekit_command_list = []

    for point in waypoints:
        command = dronekit.Command(
            0,
            0,
            0,
            MAVLINK_FRAME,
            MAVLINK_COMMAND,
            0,
            0,
            0,  # param1
            ACCEPT_RADIUS,
            0,
            0,
            point.latitude,
            point.longitude,
            altitude,
        )
        dronekit_command_list.append(command)

    return dronekit_command_list
