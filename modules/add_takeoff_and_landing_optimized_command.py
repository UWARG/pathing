"""
Prefixes a takeoff command and suffixes a landing command to the end of the list of commands with a given horizonal distance applied (for both takeoff and landing).
The horizontal distance is applied in the direction of the adjacent waypoints.
An additional buffer altitude (defaults to 0.0) is given (an initial height where climbing is fully vertical) to ensure that the drone is above a safe height for horizontal movement.
"""

import math
from . import generate_command
from .common.modules.mavlink import flight_controller
from .common.modules import position_global_relative_altitude


def add_takeoff_and_landing_optimized_command(
    commands: "list[flight_controller.dronekit.Command]", landing_pad: position_global_relative_altitude.PositionGlobalRelativeAltitude, first_waypoint: position_global_relative_altitude.PositionGlobalRelativeAltitude, last_waypoint: position_global_relative_altitude.PositionGlobalRelativeAltitude, distance: float, altitude: float, altitude_buffer: float = 1.0,
) -> "tuple[bool, list[flight_controller.dronekit.Command] | None]":
    """
    Prepends a takeoff command and appends a landing command to a list of dronekit commands with additional horizontal movement.

    Parameters
    ----------
    commands: list[flight_controller.dronekit.Command]
        Dronekit commands that can be sent to the drone.
    first_waypoint: position_global_relative_altitude.PositionGlobalRelativeAltitude
        First waypoint in the list of commands.
    last_waypoint: position_global_relative_altitude.PositionGlobalRelativeAltitude
        Last waypoint in the list of commands.
    distance: float
        Horizontal distance in meters to command the drone to during takeoff and landing.
    altitude: int
        Altitude in meters to command the drone to.
    altitude_buffer: int
        Altitude buffer in meters to command the drone to during takeoff and landing.

    Returns
    -------
    tuple[bool, list[flight_controller.dronekit.Command] | None]:
        (False, None) if empty commands list,
        (True, dronekit commands with takeoff and land commands that can be sent to the drone) otherwise.
    """
    if len(commands) == 0:
        return False, None

    takeoff_command = generate_command.takeoff(altitude_buffer)
    commands.insert(0, takeoff_command)

    # Ensure the length of the commands is at least 2
    if len(commands) < 2:
        print("Not enough commands to include horizontal distance.")
        return False, None

    # Find heading of takeoff spot and first waypoint
    first_heading = math.atan2(
        first_waypoint.latitude - landing_pad.latitude,
        first_waypoint.longitude - landing_pad.longitude,
    )

    # Find first intermediary waypoint
    first_intermediate_waypoint = generate_command.waypoint(
        landing_pad.latitude + distance * math.sin(first_heading),
        landing_pad.longitude + distance * math.cos(first_heading),
        altitude,
    )

    commands.insert(1, first_intermediate_waypoint)

    # Find heading of last waypoint and landing pad
    last_heading = math.atan2(
        last_waypoint.latitude - landing_pad.latitude,
        last_waypoint.longitude - landing_pad.longitude,
    )

    # Find last intermediary waypoint
    last_intermediate_waypoint = generate_command.waypoint(
        landing_pad.latitude + distance * math.sin(last_heading),
        landing_pad.longitude + distance * math.cos(last_heading),
        altitude_buffer,
    )

    commands.insert(len(commands) - 1, last_intermediate_waypoint)

    landing_command = generate_command.landing()
    commands.insert(len(commands), landing_command)

    return True, commands
