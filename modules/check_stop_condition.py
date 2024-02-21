"""
Checks whether the drone has reached its max flight time and sends it back to launch.
"""

import dronekit

from . import upload_commands


MAVLINK_RTL_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL
MAVLINK_RTL_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH


def check_stop_condition(start_time: float, 
                         current_time: float, 
                         drone: dronekit.Vehicle, 
                         maximum_flight_time: float) -> bool:
    """
    Check if drone exceeds the maximum flight time limit and replace with new mission of returning to launch.

    Parameters
    -----------
    start_time: float
        The time the drone started the mission in seconds.
    current_time: float
        Time elapsed in seconds since starting the mission.
    drone: dronekit.Vehicle
        The connected drone.
    maximum_flight_time: float
        Max flight time for drone in seconds. 
    
    Returns
    -------
    bool: True if max flight time was exceeded, False otherwise.
    """
    if current_time - start_time < maximum_flight_time:
        return False

    rtl_command = dronekit.Command(
        0,
        0,
        0,
        MAVLINK_RTL_FRAME,
        MAVLINK_RTL_COMMAND,
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

    # Invoke upload_commands to clear previous commands and direct drone back to launch location
    result = upload_commands.upload_commands(drone, [rtl_command])
    if not result:
        print("Unable to upload rtl command to drone command sequence.")

    return True
