"""
Method to convert list of waypoints to dronekit commands
"""
import dronekit


def waypoints_to_commands(waypoints: "list[tuple[float, float]]",
                          altitude: int) -> "list[dronekit.Command]":
    """
    Convert list of waypoints to dronekit commands

    Parameters
    ----------
    waypoints: list[tuple[float, float]]
        waypoint coordinates (latitude, longitude).
    altitude: int
        altitude in meters to command the drone to.

    Returns
    -------
    list[dronekit.Command]
        dronekit commands that can be sent to the drone.
    """
    dronekit_command_list = []

    for waypoint in waypoints:
        lat, lng = waypoint
        command = dronekit.Command(
            0,
            0,
            0,
            dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
            0,
            0,
            0,  # param1
            10,
            0,
            0,
            lat,
            lng,
            altitude,
        )
        dronekit_command_list.append(command)

    return dronekit_command_list
