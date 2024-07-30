"""
Forces drone to return to launch (RTL).
"""

# import dronekit
from modules.common.mavlink.modules.flight_controller import FlightController

from . import upload_commands
from . import generate_command

DRONE_TIMEOUT = 30.0  # seconds


def force_rtl(drone: FlightController) -> bool:
    """
    Sends RTL command using the upload_command module.

    Parameters
    -----------
    drone: FlightController
        The connected drone.

    Returns
    -------
    bool: True if uploading RTL command is successful, False otherwise.
    """

    # Generate and set RTL command
    rtl_command = generate_command.return_to_launch()

    # Utilize upload_command function to give RTL command to drone
    result = upload_commands.upload_commands(drone, [rtl_command], DRONE_TIMEOUT)

    # Error if unsuccessful
    if not result:
        print("Unable to upload RTL command to drone command sequence.")

    return result
