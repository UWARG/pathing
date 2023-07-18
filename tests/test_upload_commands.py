"""
Integration test for upload_commands.
"""

import dronekit
import math

from modules import upload_commands


MAVLINK_FRAME_GLOBAL = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
MAVLINK_WAYPOINT = dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
MAVLINK_TAKEOFF = dronekit.mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
MAVLINK_LANDING = dronekit.mavutil.mavlink.MAV_CMD_NAV_LAND  
MAVLINK_LOITER = dronekit.mavutil.mavlink.MAV_CMD_NAV_LOITER_TIME
DELAY = 3

TOLERANCE = 0.0001

CONNECTION_ADDRESS = "tcp:localhost:14550"


def retrieve_commands(drone: dronekit.Vehicle) -> dronekit.CommandSequence:
    """
    Retrieves latest version of commands.
    """
    command_sequence = drone.commands 
    command_sequence.download()
    drone.wait_ready()
    
    return command_sequence


def test_upload_command_list(drone: dronekit.Vehicle,
                             commands: "list[dronekit.Command]") -> None:
    """
    Test the case of a list of waypoint commands.
    """
    actual = upload_commands.upload_commands(drone, commands)
    assert actual

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
    actual = upload_commands.upload_commands(drone, empty_command_list)
    assert not actual
    
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

    
if __name__ == "__main__":
    # Drone setup
    drone = dronekit.connect(CONNECTION_ADDRESS, wait_ready=True)
    
    # Example waypoints list, converted to waypoint commands
    waypoints_input = [(39.140, 22.23), (25.123, -76.324)]
    altitude_input = 40

    # Test a command sequence with a variety of commands
    commands_input = []
    
    for waypoint in waypoints_input:
        lat_input, lon_input = waypoint
        command = dronekit.Command(
            0,
            0,
            0,
            MAVLINK_FRAME_GLOBAL,
            MAVLINK_WAYPOINT,
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

    loiter_command = dronekit.Command(
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
    commands_input.append(loiter_command)

    # Test with the command sequence
    test_upload_command_list(drone, commands_input)

    # Test with empty command sequence
    test_upload_empty_command_list(drone)

    print("Done!")
