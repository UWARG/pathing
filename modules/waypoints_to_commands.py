"""
Function to convert list of waypoints to dronekit commands
"""

import dronekit


MAVLINK_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
ACCEPT_RADIUS = 10


def waypoints_to_commands(waypoints: "list[tuple[float, float]]",
                          altitude: int) -> "tuple[bool, list[dronekit.Command] | None]":
    """
    Convert list of waypoints to dronekit commands.

    Parameters
    ----------
    waypoints: list[tuple[float, float]]
        waypoint coordinates in decimal degrees (latitude, longitude).
    altitude: int
        altitude in meters to command the drone to.

    Returns
    -------
    tuple[bool, list[dronekit.Command] | None]: 
        (False, None) if empty waypoints list,
        (True, dronekit commands that can be sent to the drone) otherwise
        dronekit commands that can be sent to the drone.
    """
    if len(waypoints) == 0:
        return False, None

    dronekit_command_list = []

    for waypoint in waypoints:
        lat, lng = waypoint
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
            lat,
            lng,
            altitude,
        )
        dronekit_command_list.append(command)

    return True, dronekit_command_list
