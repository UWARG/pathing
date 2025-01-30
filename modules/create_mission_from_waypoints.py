"""
Function that appends waypoints for N laps to create a mission
"""

from . import waypoints_to_commands
from .common.modules import location_global
from .common.modules.mavlink import flight_controller


def create_mission_from_waypoints(
    num_laps: int,
    takeoff_altitude: int,
    laps_altitude: int,
    start_sequence_list: list[location_global.LocationGlobal],
    lap_sequence_list: list[location_global.LocationGlobal],
) -> tuple[True, list[flight_controller.dronekit.Command]] | tuple[False, None]:
    """
    Creates a mission(list of flight_controller (dronekit) commands) from starting sequence waypoints
    and lap sequence waypoints repeated N times

    num_laps: The number of laps to run.
    takeoff_altitude: Drone's altitude in metres for takeoff.
    laps_altitude: Drone's altitude in metres for laps.
    start_seqeunce_list: A list of waypoints for the starting sequence.
    lap_sequence_list: A list of waypoints representing one lap.

    Return: Success, list of commands that represent the mission.
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
    success, laps_commands = waypoints_to_commands.waypoints_to_commands(laps_list, laps_altitude)
    if not success:
        return False, None

    # Create and return the mission flight_controller (dronekit) commands
    mission_waypoints_commands = takeoff_commands + laps_commands

    return True, mission_waypoints_commands
