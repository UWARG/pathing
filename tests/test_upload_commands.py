"""
Integration test for upload_commands.
"""

import dronekit

from modules import upload_commands


MAVLINK_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
MAVLINK_TAKEOFF = dronekit.mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
MAVLINK_LANDING = dronekit.mavutil.mavlink.MAV_CMD_NAV_LAND
DELAY = 3
CONNECTION_ADDRESS = "tcp:localhost:14550"
TOLERANCE = 0.00001


def test_upload_waypoint_command_list(drone: dronekit.Vehicle,
                                      commands: "list[dronekit.Command]") -> None:
    """
    Test the case of a list of waypoint commands.
    """
    upload_commands.upload_commands(drone,commands)

    # Retrieve current drone commands and see if they match with inputs
    command_sequence = drone.commands
    command_sequence.download()
    command_sequence.wait_ready()
    
    for i, command in enumerate(command_sequence):
        lat_input = waypoints_input[i][0]
        lon_input = waypoints_input[i][1]
        
        assert command.frame == MAVLINK_FRAME
        assert command.command == MAVLINK_COMMAND
        assert command.param1 == DELAY
        # Parameters 2,3,4 not being tested since Mission Planner ignores them
        assert command.param2 == 0 
        assert command.param3 == 0
        assert command.param4 == 0
        assert abs(command.x - lat_input) <= TOLERANCE 
        assert abs(command.y - lon_input) <= TOLERANCE
        assert command.z == altitude_input


def test_upload_empty_command_list(drone: dronekit.Vehicle,
                                   commands: "list[dronekit.Command]") -> None:
    """
    Test the case of an empty command list.
    """
    upload_commands.upload_commands(drone,commands)

    # Retrieve current drone commands and see if they match with previous inputs
    command_sequence = drone.commands 
    command_sequence.download()
    drone.wait_ready()

    for i, command in enumerate(command_sequence):
        lat_input = waypoints_input[i][0]
        lon_input = waypoints_input[i][1]

        assert command.frame == MAVLINK_FRAME
        assert command.command == MAVLINK_COMMAND
        assert command.param1 == DELAY
        # Parameters 2,3,4 not being tested since Mission Planner ignores them
        assert command.param2 == 0
        assert command.param3 == 0
        assert command.param4 == 0
        assert abs(command.x - lat_input) <= TOLERANCE
        assert abs(command.y - lon_input) <= TOLERANCE
        assert command.z == altitude_input

        
def test_upload_takeoff_command(drone: dronekit.Vehicle,
                                 commands: "list[dronekit.Command]") -> None:
    """
    Test the case of a takeoff command.
    """
    upload_commands.upload_commands(drone,commands)

    # Retrieve current drone commands and see if they match with previous inputs
    command_sequence = drone.commands 
    command_sequence.download()
    drone.wait_ready()

    for command in command_sequence:
        assert command.frame == MAVLINK_FRAME
        assert command.command == MAVLINK_TAKEOFF
        assert command.param1 == 0
        assert command.param2 == 0
        assert command.param3 == 0
        assert command.param4 == 0
        assert command.x == 0
        assert command.y == 0
        assert command.z == altitude_input
    

def test_upload_landing_command(drone: dronekit.Vehicle,
                                 commands: "list[dronekit.Command]") -> None:
    """
    Test the case of a landing command.
    """
    upload_commands.upload_commands(drone,commands)

    # Retrieve current drone commands and see if they match with previous inputs
    command_sequence = drone.commands 
    command_sequence.download()
    drone.wait_ready()

    for command in command_sequence:
        assert command.frame == MAVLINK_FRAME
        assert command.command == MAVLINK_LANDING
        assert command.param1 == 0
        assert command.param2 == 0
        assert command.param3 == 0
        assert command.param4 == 0
        assert command.x == 0
        assert command.y == 0
        assert command.z == 0

    
if __name__ == "__main__":
    # Drone setup
    drone = dronekit.connect(CONNECTION_ADDRESS, wait_ready=True)
    commands_input = []
    
    # Example waypoints list, converted to waypoint commands
    waypoints_input = [(39.140, 22.23), (25.123, -76.324)]
    altitude_input = 40

    # Test with waypoint command sequence
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
            DELAY,
            0,
            0,
            0,
            lat_input,
            lon_input,
            altitude_input,
        )
        commands_input.append(command)
    test_upload_waypoint_command_list(drone,commands_input)

    # Test with empty command sequence
    commands_input = []
    test_upload_empty_command_list(drone,commands_input)

    # Test with takeoff command
    commands_input = []
    takeoff_command = dronekit.Command(
        0,
        0,
        0,
        MAVLINK_FRAME,
        MAVLINK_TAKEOFF,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        altitude_input,
    )
    commands_input.append(takeoff_command)
    test_upload_takeoff_command(drone,commands_input)
    
    # Test with landing command
    commands_input = []
    landing_command = dronekit.Command(
        0,
        0,
        0,
        MAVLINK_FRAME,
        MAVLINK_LANDING,
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
    commands_input.append(landing_command)
    test_upload_landing_command(drone,commands_input)
    
    print("Done!")
