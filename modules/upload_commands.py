"""
Function to upload dronekit commands.
"""

import dronekit


def upload_commands(drone: dronekit.Vehicle, commands: "list[dronekit.Command]") -> None:
    """
    Add the list of commands to the drone’s command sequence, and upload them.
    If the list is empty, does not upload anything.

    Parameters
    -----------
    drone: dronekit.Vehicle
        The connected drone.
    commands: list[dronekit.Command]
        List of dronekit commands.

    Returns
    -------
    None
    """
    # If the list is empty, do nothing
    if len(commands) == 0:
        return
       
    # Download the command sequence and clear it
    # This is to avoid duplicate or conflicting commands
    command_sequence = drone.commands
    command_sequence.download()
    command_sequence.wait_ready()
    command_sequence.clear()

    # Adds new commands to command sequence
    for command in commands:
        command_sequence.add(command)

    # Upload the commands to drone
    command_sequence.upload()
