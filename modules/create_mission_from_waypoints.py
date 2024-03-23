"""
Function that appends waypoints for N laps to create a mission
"""

import dronekit

from . import waypoints_to_commands
from .common.kml.modules import location_ground


def create_mission_from_waypoints(num_laps: int,
                                  altitude:int,
                                  start_sequence_list: "list[location_ground.LocationGround]",
                                  lap_sequence_list: "list[location_ground.LocationGround]")\
                                  ->  "tuple[bool, list[dronekit.Command] | None]" :
    """
    Creates a mission(list of dronekit commands) from starting sequence waypoints 
    and lap sequence waypoints repeated N times

    Parameters:
        - num_laps (int): The number of laps to run
        - altitude (int): Altitude in meters to command the drone to
        - start_seqeunce_list (list[LocationGround]): A list of waypoints for the starting sequence
        - lap_sequence_list (list[LocationGround]): A list of waypoints representing one lap

    Returns:
        - (False, None): If there is an error in converting the waypoints into commands
        - (True, mission_waypoints_commands): A list of dronekit commands that represent the mission
    """
    #load in the starting sequence
    mission_waypoints_list = start_sequence_list.copy()

    # Append the lap sequence n times
    for _ in range(num_laps):
        mission_waypoints_list += lap_sequence_list

    # Convert the mission waypoints list to dronekit commands
    success, mission_waypoints_commands = waypoints_to_commands.waypoints_to_commands(mission_waypoints_list, altitude)
    if not success:
        return False, None

    return True, mission_waypoints_commands
