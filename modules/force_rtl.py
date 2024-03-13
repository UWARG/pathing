"""
Forces RTL (return to landing)
"""

import dronekit

from . import upload_commands

MAVLINK_RTL_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL
MAVLINK_RTL_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH


def force_rtl(drone: dronekit.Vehicle)->None:
    """
    Clear current drone mission, sends RTL command using upload_command module
    
    Parameters
    -----------
    drone: dronekit.Vehicle
        The connected drone.

    Returns
    -------
    None
    """

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

    # upload RTL command
    success = upload_commands.upload_commands(drone, [rtl_command])
    # error if unsuccessful
    if not success:
        print("Unable to upload RTL command to drone command sequence.")