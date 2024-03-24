"""
Function that appends waypoints for N laps to create a mission
"""

import dronekit

from . import waypoints_to_commands
from .common.kml.modules import location_ground


def create_mission_from_waypoints(
    num_laps: int,
    takeoff_altitude: int,
    laps_altitude: int,
    start_sequence_list: "list[location_ground.LocationGround]",
    lap_sequence_list: "list[location_ground.LocationGround]",
) -> "tuple[bool, list[dronekit.Command] | None]":
    """
    Creates a mission(list of dronekit commands) from starting sequence waypoints
    and lap sequence waypoints repeated N times

    Parameters:
        - num_laps (int): The number of laps to run
        - takeoff_altitude (int): Drone's altitude in metres for takeoff
        - laps_altitude (int): Drone's altitude in metres for laps
        - start_seqeunce_list (list[LocationGround]): A list of waypoints for the starting sequence
        - lap_sequence_list (list[LocationGround]): A list of waypoints representing one lap

    Returns:
        - (False, None): If there is an error in converting any waypoints into commands
        - (True, mission_waypoints_commands): A list of dronekit commands that represent the mission
    """
    # convert the starting sequence into a list of commands
    success, takeoff_commands = waypoints_to_commands.waypoints_to_commands(
        start_sequence_list, takeoff_altitude
    )
    if not success:
        return False, None

    # Append the lap sequence n times
    laps_list = []
    for _ in range(num_laps):
        laps_list += lap_sequence_list

    # Convert the laps list into a list of commands
    success, laps_commands = waypoints_to_commands.waypoints_to_commands(
        laps_list, laps_altitude
    )
    if not success:
        return False, None

    # Create and return the mission dronekit commands
    mission_waypoints_commands = takeoff_commands + laps_commands

    return True, mission_waypoints_commands
