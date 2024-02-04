"""
Checks whether the drone has reached it's max flight time and sends it back to launch.
"""

import dronekit

from . import upload_commands


MAVLINK_LANDING_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL
MAVLINK_LANDING_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH


def check_stop_condition(start_time: float, current_time: float, drone: dronekit.Vehicle, MAXIMUM_FLIGHT_TIME: int)\
    -> bool:
    """
    Check if drone exceeds the maximum flight time limit and replace with new mission of returning to launch.

    Parameters
    -----------
    start_time: float
        The time at which the drone loop in path_2024.py began.
    current_time: float
        Total elapsed time for program.
    drone: dronekit.Vehicle
        The connected drone.
    MAXIMUM_FLIGHT_TIME: int
        max flight time for drone in seconds 
    
    Returns
    -------
    bool: True if max flight time was exceeded, False otherwise
    """
    if current_time - start_time < MAXIMUM_FLIGHT_TIME:
        return False

    landing_command = dronekit.Command(
        0,
        0,
        0,
        MAVLINK_LANDING_FRAME,
        MAVLINK_LANDING_COMMAND,
        0,
        0,
        0,  # param1
        0,
        0,
        0,
        0,
        0,
        0,
    )

    # Invoke upload_commands to clear previous commands and direct drone back to launch
    upload_commands.upload_commands(drone, list(landing_command))

    return True
