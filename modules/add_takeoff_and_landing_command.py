"""
Prefixes a takeoff command and suffixes a landing command to the end of the list of commands.
"""

from . import generate_command
from .common.modules.mavlink import flight_controller


def add_takeoff_and_landing_command(
    commands: "list[flight_controller.dronekit.Command]", altitude: float
) -> "tuple[bool, list[flight_controller.dronekit.Command] | None]":
    """
    Prepends a takeoff command and appends a landing command to a list of flight_controller.dronekit commands.

    Parameters
    ----------
    commands: list[flight_controller.dronekit.Command]
        Dronekit commands that can be sent to the drone.
    altitude: int
        Altitude in meters to command the drone to.

    Returns
    -------
    tuple[bool, list[flight_controller.dronekit.Command] | None]:
        (False, None) if empty commands list,
        (True, flight_controller.dronekit commands with takeoff and land commands that can be sent to the drone) otherwise.
    """
    if len(commands) == 0:
        return False, None

    takeoff_command = generate_command.takeoff(altitude)
    commands.insert(0, takeoff_command)

    landing_command = generate_command.landing()
    commands.append(landing_command)

    return True, commands
