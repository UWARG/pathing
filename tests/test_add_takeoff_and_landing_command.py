"""
Test process
"""
import copy

import dronekit
import pytest

from modules import add_takeoff_and_landing_command


ALTITUDE = 50
MAVLINK_TEST_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
MAVLINK_TEST_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL
ACCEPT_RADIUS = 10


@pytest.fixture
def non_empty_commands() -> "list[dronekit.Command]":
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
            ACCEPT_RADIUS,
            0,
            0,
            42.123,
            -73.456,
            ALTITUDE,
        ),
        dronekit.Command(
            0,
            0,
            0,
            MAVLINK_TEST_FRAME,
            MAVLINK_TEST_COMMAND,
            0,
            0,
            0,  # param1
            ACCEPT_RADIUS,
            0,
            0,
            42.789,
            -73.987,
            ALTITUDE,
        )
    ]
    yield commands


@pytest.fixture
def empty_commands() -> "list[dronekit.Command]":
    """
    Fixture for an empty list of commands.
    """
    commands = []
    yield commands


def assert_expected_takeoff_and_landing_commands(commands_actual: "list[dronekit.Command]",
                                                 commands_expected: "list[dronekit.Command]",
                                                 altitude: float):
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

    # Test original commands
    assert len(commands_actual) == len(commands_expected) + 2
    for i in range(len(commands_expected)):
        assert commands_actual[i+1] == commands_expected[i]


def test_add_takeoff_and_landing_on_empty_commands(empty_commands: "list[dronekit.Command]"):
    """
    Tests functionality correctness of add_takeoff_and_landing_command on empty list of commands.
    """
    commands_expected = copy.deepcopy(empty_commands)
    commands_actual = add_takeoff_and_landing_command.add_takeoff_and_landing_command(empty_commands, ALTITUDE)
    assert_expected_takeoff_and_landing_commands(commands_actual, commands_expected, ALTITUDE)


def test_add_takeoff_and_landing_on_nonempty_commands(non_empty_commands: "list[dronekit.Command]"):
    """
    Tests functionality correctness of add_takeoff_and_landing_command on non-empty list of commands.
    """
    commands_expected = copy.deepcopy(non_empty_commands)
    commands_actual = add_takeoff_and_landing_command.add_takeoff_and_landing_command(non_empty_commands, ALTITUDE)
    assert_expected_takeoff_and_landing_commands(commands_actual, commands_expected, ALTITUDE)