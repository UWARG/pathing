"""
Test process
"""

import dronekit
import pytest

from modules import add_takeoff_and_landing_command


ALTITUDE = 50
MAVLINK_TEST_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
MAVLINK_TEST_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL


@pytest.fixture
def non_empty_commands():
    """
    Fixture for a list of commands.
    """
    commands = [
        dronekit.Command(
            0,
            0,
            0,
            MAVLINK_TEST_FRAME,
            MAVLINK_TEST_COMMAND,
            0,
            0,
            0,  # param1
            0,
            0,
            0,
            0,
            0,
            0,
        ),
        dronekit.Command(
            0,
            0,
            0,
            MAVLINK_TEST_FRAME,
            MAVLINK_TEST_FRAME,
            0,
            0,
            0,  # param1
            0,
            0,
            0,
            0,
            0,
            0,
        )
    ]
    return commands


@pytest.fixture
def empty_commands():
    """
    Fixture for an empty list of commands.
    """
    commands = []
    return commands


def assert_takeoff_and_landing_commands(commands_input, commands_actual, altitude):
    """
    Helper function to assert the correctness of takeoff and landing commands.
    """
    assert isinstance(commands_actual, list)

    # Test takeoff command
    takeoff_command = commands_actual[0]
    assert isinstance(takeoff_command, dronekit.Command)
    assert takeoff_command.frame == add_takeoff_and_landing_command.MAVLINK_TAKEOFF_FRAME
    assert takeoff_command.command == add_takeoff_and_landing_command.MAVLINK_TAKEOFF_COMMAND
    assert takeoff_command.z == altitude

    # Test landing command
    landing_command = commands_actual[-1]
    assert isinstance(landing_command, dronekit.Command)
    assert landing_command.frame == add_takeoff_and_landing_command.MAVLINK_LANDING_FRAME
    assert landing_command.command == add_takeoff_and_landing_command.MAVLINK_LANDING_COMMAND


def test_add_takeoff_and_landing_on_empty_commands(empty_commands):
    """
    Tests functionality correctness of add_takeoff_and_landing_command on empty list of commands.
    """
    commands_actual = add_takeoff_and_landing_command.add_takeoff_and_landing_command(empty_commands, ALTITUDE)
    assert_takeoff_and_landing_commands(empty_commands, commands_actual, ALTITUDE)


def test_add_takeoff_and_landing_on_nonempty_commands(non_empty_commands):
    """
    Tests functionality correctness of add_takeoff_and_landing_command on non-empty list of commands.
    """
    commands_actual = add_takeoff_and_landing_command.add_takeoff_and_landing_command(non_empty_commands, ALTITUDE)
    assert_takeoff_and_landing_commands(non_empty_commands, commands_actual, ALTITUDE)
