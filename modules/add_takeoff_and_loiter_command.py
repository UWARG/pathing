"""
Prefixes a takeoff command and suffixes a loiter command to the end of the list of commands.
"""

from . import generate_command
from .common.modules.mavlink import flight_controller


def add_takeoff_and_loiter_command(
    commands: "list[flight_controller.dronekit.Command]",
    latitude: float,
    longitude: float,
    takeoff_altitude: float,
    loiter_altitude: float,
) -> "tuple[bool, list[flight_controller.dronekit.Command] | None]":
    """
    Prepends a takeoff command and appends a loiter command to a list of dronekit commands.

    Parameters
    ----------
    commands: list[flight_controller.dronekit.Command]
        dronekit commands that can be sent to the drone.
    latitude: float
        Loiter latitude values
    longitude: float
        Loiter longitude values
    altitude: float
        Altitude in meters to command the drone to during takeoff.

    Returns
    -------
    tuple[bool, list[flight_controller.dronekit.Command] | None]:
        (False, None) if empty commands list,
        (True, dronekit commands with takeoff and land commands that can be sent to the drone) otherwise.
    """
    if len(commands) == 0:
        return False, None

    takeoff_command = generate_command.takeoff(takeoff_altitude)
    commands.insert(0, takeoff_command)

    loiter_command = generate_command.loiter_unlimited(latitude, longitude, loiter_altitude)
    commands.append(loiter_command)

    return True, commands
