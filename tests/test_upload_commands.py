"""
Testcases for upload_commands.
"""

import dronekit

from modules import upload_commands


MAVLINK_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
ACCEPT_RADIUS = 10


# Drone setup
connection_address = "tcp:localhost:14550"
drone = dronekit.connect(connection_address, wait_ready=True)
commands_input = drone.commands
commands_input.clear()

# Example waypoints list, converted to waypoint commands
waypoints_input = [(39.140, -86.23), (21.731, -91.9), (11.255, 53.825)]
altitude_input = 40

for waypoint in waypoints_input:
    lat_input, lon_input = waypoint
    command = dronekit.Command(
        0,
        0,
        0,
        MAVLINK_FRAME,
        MAVLINK_COMMAND,
        0,
        0,
        0,
        ACCEPT_RADIUS,
        0,
        0,
        lat_input,
        lon_input,
        altitude_input,
    )
    commands_input.add(command)

        
def test_upload_commands():
    """
    Integration test for upload_commands.
    """
    # Run upload_commands
    upload_commands.upload_commands(drone,commands_input)

    # Retrieve current drone commands and see if they match with inputs
    for i, command in enumerate(drone.commands):
        lat_input = waypoints_input[i][0]
        lon_input = waypoints_input[i][1]

        assert command.frame == MAVLINK_FRAME
        assert command.command == MAVLINK_COMMAND
        assert command.param1 == 0
        assert command.param2 == ACCEPT_RADIUS
        assert command.param3 == 0
        assert command.param4 == 0
        assert command.x == lat_input
        assert command.y == lon_input
        assert command.z == altitude_input


def test_upload_empty_command_list():
    # Run upload_commands on empty command list
    commands_input.clear()
    upload_commands.upload_commands(drone,commands_input)

    # Retrieve current drone commands and see if they match with previous inputs
    for i, command in enumerate(drone.commands):
        lat_input = waypoints_input[i][0]
        lon_input = waypoints_input[i][1]

        assert command.frame == MAVLINK_FRAME
        assert command.command == MAVLINK_COMMAND
        assert command.param1 == 0
        assert command.param2 == ACCEPT_RADIUS
        assert command.param3 == 0
        assert command.param4 == 0
        assert command.x == lat_input
        assert command.y == lon_input
        assert command.z == altitude_input
        
    
def main():
    test_upload_commands()
    test_upload_empty_command_list()
    print("Done!")
