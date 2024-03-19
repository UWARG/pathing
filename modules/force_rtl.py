"""
Forces drone to return to launch (RTL).
"""

import dronekit

from . import upload_commands

MAVLINK_RTL_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL
MAVLINK_RTL_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH


def force_rtl(drone: dronekit.Vehicle) -> bool:
    """
    Sends RTL command using the upload_command module.
    
    Parameters
    -----------
    drone: dronekit.Vehicle
        The connected drone.

    Returns
    -------
    bool: True if uploading RTL command is successful, False otherwise.
    """

    # clears current mission
    rtl_command = dronekit.Command(
        0,
        0,
        0,
        MAVLINK_RTL_FRAME,
        MAVLINK_RTL_COMMAND,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    
    # utilize upload_command function to give RTL command to drone
    result = upload_commands.upload_commands(drone, [rtl_command])
    
    # error if unsuccessful
    if not result:
        print("Unable to upload RTL command to drone command sequence.")
        
    return result