"""
Prefixes a takeoff command and suffixes a landing command to the end of the list of commands.
"""

import dronekit

from . import generate_command


def add_takeoff_and_landing_command(
    commands: "list[dronekit.Command]", altitude: float
) -> "tuple[bool, list[dronekit.Command] | None]":
    """
    Prepends a takeoff command and appends a landing command to a list of dronekit commands.

    Parameters
    ----------
    commands: list[dronekit.Command]
        Dronekit commands that can be sent to the drone.
    altitude: int
        Altitude in meters to command the drone to.

    Returns
    -------
    tuple[bool, list[dronekit.Command] | None]:
        (False, None) if empty commands list,
        (True, dronekit commands with takeoff and land commands that can be sent to the drone) otherwise.
    """
    if len(commands) == 0:
        return False, None

    takeoff_command = generate_command.takeoff(altitude)
    commands.insert(0, takeoff_command)

    landing_command = generate_command.landing()
    commands.append(landing_command)

    return True, commands
