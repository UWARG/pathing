"""
Integration test for upload_commands.
"""

import math

import dronekit

from modules import generate_command
from modules import upload_commands


ALTITUDE = 40
DRONE_TIMEOUT = 30.0  # seconds

WAYPOINT_HOLD_TIME = 3.0  # seconds
ACCEPT_RADIUS = 10.0  # metres

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


def upload_command_list_and_assert(
    drone: dronekit.Vehicle, commands: "list[dronekit.Command]"
) -> None:
    """
    Test the case of a list of waypoint commands.
    """
    result = upload_commands.upload_commands(drone, commands, DRONE_TIMEOUT)
    assert result

    # Retrieve current drone commands and see if they match with inputs
    command_sequence = retrieve_commands(drone)

    for i, command in enumerate(command_sequence):
        assert command.frame == commands[i].frame
        assert command.command == commands[i].command
        assert command.param1 == commands[i].param1
        # Parameters 2,3,4 not being tested since Mission Planner ignores them
        assert math.isclose(command.x, commands[i].x, abs_tol=TOLERANCE)
        assert math.isclose(command.y, commands[i].y, abs_tol=TOLERANCE)
        assert math.isclose(command.z, commands[i].z, abs_tol=TOLERANCE)


def upload_empty_command_list_and_assert(drone: dronekit.Vehicle) -> None:
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
    result = upload_commands.upload_commands(drone, empty_command_list, DRONE_TIMEOUT)
    assert not result

    # Retrieve new commands and compare them with previous list
    command_check = retrieve_commands(drone)

    for i, command in enumerate(command_check):
        assert command.frame == commands[i].frame
        assert command.command == commands[i].command
        assert command.param1 == commands[i].param1
        # Parameters 2,3,4 not being tested since Mission Planner ignores them
        assert math.isclose(command.x, commands[i].x, abs_tol=TOLERANCE)
        assert math.isclose(command.y, commands[i].y, abs_tol=TOLERANCE)
        assert math.isclose(command.z, commands[i].z, abs_tol=TOLERANCE)


def main() -> int:
    """
    Main function.
    """
    # Drone setup
    # Wait ready is false as the drone may be on the ground
    dronekit_vehicle = dronekit.connect(CONNECTION_ADDRESS, wait_ready=False)

    # Example waypoints list, converted to waypoint commands
    waypoints_input = [(39.140, 22.23), (25.123, -76.324)]

    # Test a command sequence with a variety of commands
    commands_input = []

    for waypoint in waypoints_input:
        lat_input, lon_input = waypoint
        dronekit_command = generate_command.waypoint(
            WAYPOINT_HOLD_TIME, ACCEPT_RADIUS, lat_input, lon_input, ALTITUDE
        )
        commands_input.append(dronekit_command)

    takeoff_command = generate_command.takeoff(ALTITUDE)
    commands_input.append(takeoff_command)

    landing_command = generate_command.landing()
    commands_input.append(landing_command)

    # Test with the command sequence
    upload_command_list_and_assert(dronekit_vehicle, commands_input)

    # Test with empty command sequence
    upload_empty_command_list_and_assert(dronekit_vehicle)

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
