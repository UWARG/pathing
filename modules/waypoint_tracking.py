"""
Module for obtaining information about the drone,
including the current waypoint sequence, location, and destination.
"""

import dronekit


def get_current_waypoint_info(drone: dronekit.Vehicle) -> "tuple[bool, tuple[int, tuple[float, float]]]":
    """
    Function to retrieve information about the current waypoint sequence and destination
    """
    # Download the mission commands from the drone
    drone.commands.download()
    drone.commands.wait_ready()

    # Get the current waypoint sequence
    current_waypoint = drone.commands.next
    waypoint_info = (current_waypoint, None)

    # Get the current destination
    if current_waypoint < len(drone.commands):
        current_command = drone.commands[current_waypoint]
        if current_command.command == dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT:
            waypoint_info = (current_waypoint, (current_command.x, current_command.y))
    return waypoint_info


def get_current_location(drone: dronekit.Vehicle) -> "tuple[bool, tuple[float, float]]":
    """
    Function to retrieve the current location (latitude and longitude) of the drone
    """
    curr_waypoint_info = get_current_waypoint_info(drone)

    # Get the current location (latitude, longitude)
    current_location = drone.location.global_frame
    if current_location is None:
        return False, None

    return True, (current_location.lat, current_location.lon)
