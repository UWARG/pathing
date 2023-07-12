"""
Function to upload dronekit commands
"""


import dronekit


def upload_commands(drone: dronekit.Vehicle, commands: "list[dronekit.Command]") -> None:
    """
    Add the list of commands to the drone’s command sequence, and upload them.

    Parameters
    -----------
    drone: dronekit.Vehicle
        the connected drone.
    commands: list[dronekit.Command]
        list of dronekit commands.

    Returns
    -------
    None
    """
    # Get the set of commands from the drone
    command_sequence = drone.commands
    command_sequence.download()
    command_sequence.wait_ready()
    command_sequence.clear()
    for command in commands:
        command_sequence.add(command)

    # Upload the commands to drone
    command_sequence.upload()
    





    
