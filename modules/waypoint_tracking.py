"""
Module for obtaining information about the drone,
including the current waypoint sequence, location, and destination.
"""

# import dronekit
from modules.common.mavlink.modules.flight_controller import FlightController


def get_current_waypoint_info(
    controller: FlightController,
) -> "tuple[bool, tuple[int, tuple[float, float] | None] | None]":
    """
    Function to retrieve information about the current waypoint sequence and destination

    Parameters
    ----------
    controller: FlightController
        The connected drone.

    Returns
    -------
    tuple[bool, tuple[int, tuple[float, float] | None] | None]:
        (True, destination waypoint information), where information is (index, location).
        location can be None.
    """

    # Get the current waypoint sequence
    download_success, current_waypoint = controller.download_commands()
    if download_success:
        waypoint_info = (current_waypoint, None)
    else:
        return False, (None, None)

    # Get the current destination
    if current_waypoint < controller.commands.count:
        current_command = controller.commands[current_waypoint]
        success, destination_reached = controller.is_drone_destination_final_waypoint()
        waypoint_info = (current_waypoint, (current_command.x, current_command.y))

    return (True, waypoint_info) if success and destination_reached else (False, waypoint_info)


def get_current_location(controller: FlightController) -> "tuple[bool, tuple[float, float] | None]":
    """
    Function to retrieve the current location (latitude and longitude) of the drone

    Parameters
    ----------
    controller: FlightController
        The connected drone.

    Returns
    -------
    tuple[bool, tuple[float, float] | None]:
        (True, current location), where location is (latitude, longitude).
        location can be None.
    """
    # Get the current location (latitude, longitude)
    current_location = controller.location.global_frame
    if current_location is None:
        return False, None

    return True, (current_location.lat, current_location.lon)
