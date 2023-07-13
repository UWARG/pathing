"""
Testcases for upload_commands.
"""

import dronekit

from modules import waypoints_to_commands


def test_upload_commands():
    """
    Integration test for upload_commands.
    """
    # Example waypoints list, converted to waypoint commands
    waypoints_input = [(39.140, -86.23), (21.731, -91.9), (11.255, 53.825)]
    altitude_input = 40
    commands_input = waypoints_to_commands.waypoints_to_commands(waypoints_input, altitude_input)
    connection_address = "tcp:localhost:14550"
    drone = dronekit.connect(connection_address, wait_ready=True)
    commands = commands_input

    # upload_commands
    if (len(commands) == 0):
        pass
    else:    
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


    for i, command in enumerate(command_sequence):
        lat_input = waypoints_input[i][0]
        lon_input = waypoints_input[i][1]

        assert command.frame == waypoints_to_commands.MAVLINK_FRAME
        assert command.command == waypoints_to_commands.MAVLINK_COMMAND
        assert command.param1 == 0
        assert command.param2 == waypoints_to_commands.ACCEPT_RADIUS
        assert command.param3 == 0
        assert command.param4 == 0
        assert command.x == lat_input
        assert command.y == lon_input
        assert command.z == altitude_input

    # Test for empty command list
    commands.clear()

    # upload_commands
    if (len(commands) == 0):
        pass
    else:    
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
        
    assert command.frame == waypoints_to_commands.MAVLINK_FRAME
    assert command.command == waypoints_to_commands.MAVLINK_COMMAND
    assert command.param1 == 0
    assert command.param2 == waypoints_to_commands.ACCEPT_RADIUS
    assert command.param3 == 0
    assert command.param4 == 0
    assert command.x == lat_input
    assert command.y == lon_input
    assert command.z == altitude_input
