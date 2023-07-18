"""
Integration test for upload_commands.
"""

import dronekit
import math

from modules import upload_commands


MAVLINK_FRAME_GLOBAL = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_NAV_WAYPOINT = dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
MAVLINK_TAKEOFF = dronekit.mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
MAVLINK_LANDING = dronekit.mavutil.mavlink.MAV_CMD_NAV_LAND  
MAVLINK_LOITER = dronekit.mavutil.mavlink.MAV_CMD_NAV_LOITER_TIME
DELAY = 3
TOLERANCE = 0.0001

CONNECTION_ADDRESS = "tcp:localhost:14550"

    
def test_upload_command_list(drone: dronekit.Vehicle,
                                      commands: "list[dronekit.Command]") -> None:
    """
    Test the case of a list of waypoint commands.
    """
    upload_commands.upload_commands(drone, commands)

    # Retrieve current drone commands and see if they match with inputs
    command_sequence = retrieve_commands(drone)
    
    for i, command in enumerate(command_sequence):
        assert command.frame == commands[i].frame
        assert command.command == commands[i].command
        assert command.param1 == commands[i].param1
        # Parameters 2,3,4 not being tested since Mission Planner ignores them
        assert math.isclose(command.x, commands[i].x, abs_tol = TOLERANCE)
        assert math.isclose(command.y, commands[i].y, abs_tol = TOLERANCE)
        assert math.isclose(command.z, commands[i].z, abs_tol = TOLERANCE)


def test_upload_empty_command_list(drone: dronekit.Vehicle) -> None:
    """
    Test the case of an empty command list.
    """
    # Retrieve current drone commands and add them to a list
    command_sequence = retrieve_commands(drone)
    commands = []
    for command in command_sequence:
        commands.append(command)

    # Upload empty command list
    empty_command_list = []
    upload_commands.upload_commands(drone, empty_command_list)

    # Retrieve new commands and compare them with previous list
    command_check = retrieve_commands(drone)
    
    for i, command in enumerate(command_check):
        assert command.frame == commands[i].frame
        assert command.command == commands[i].command
        assert command.param1 == commands[i].param1
        # Parameters 2,3,4 not being tested since Mission Planner ignores them
        assert math.isclose(command.x, commands[i].x, abs_tol = TOLERANCE)
        assert math.isclose(command.y, commands[i].y, abs_tol = TOLERANCE)
        assert math.isclose(command.z, commands[i].z, abs_tol = TOLERANCE)


def retrieve_commands(drone: dronekit.Vehicle) -> dronekit.CommandSequence:
    """
    Retrieves latest version of commands.
    """
    command_sequence = drone.commands 
    command_sequence.download()
    drone.wait_ready()
    
    return command_sequence

    
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
            MAVLINK_FRAME_GLOBAL,
            MAVLINK_NAV_WAYPOINT,
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
    test_upload_command_list(drone,commands_input)

    # Test with empty command sequence
    commands_input = []
    test_upload_empty_command_list(drone)

    # Test with takeoff command
    commands_input = []
    takeoff_command = dronekit.Command(
        0,
        0,
        0,
        MAVLINK_FRAME_GLOBAL,
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
    test_upload_command_list(drone,commands_input)
    
    # Test with landing command
    commands_input = []
    landing_command = dronekit.Command(
        0,
        0,
        0,
        MAVLINK_FRAME_GLOBAL,
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
    test_upload_command_list(drone,commands_input)

    # Test with loiter time command
    commands_input = []
    loiter_time_command = dronekit.Command(
    0,                          
    0,                          
    0,                          
    MAVLINK_FRAME_GLOBAL,  
    MAVLINK_LOITER,         
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
    commands_input.append(landing_command)
    test_upload_command_list(drone,commands_input)
    
    print("Done!")
