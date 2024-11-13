"""
Forces drone to return to launch (RTL).
"""

from . import generate_command
from .common.modules.mavlink import flight_controller


def force_rtl(controller: flight_controller.FlightController) -> bool:
    """
    Sends RTL command using the upload_command module.

    controller: The connected drone's flight controller instance.

    Return: True if uploading RTL command is successful, False otherwise.
    """

    # Generate and set RTL command
    rtl_command = generate_command.return_to_launch()

    # Change drone mode
    result = controller.set_flight_mode("RTL")

    if not result:
        print("Unable to set drone mode to RTL.")
        return result

    # Utilize upload_command function to give RTL command to drone
    result = controller.upload_commands([rtl_command])

    if not result:
        print("Unable to upload RTL command to drone command sequence.")

    return result
