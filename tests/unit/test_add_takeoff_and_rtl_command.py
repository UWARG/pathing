"""
Test process.
"""

import copy

from pymavlink import mavutil
import pytest

from modules import add_takeoff_and_rtl_command
from modules import generate_command
from modules.common.modules.mavlink import dronekit


ALTITUDE = 50.0  # metres
ACCEPT_RADIUS = 10.0  # metres
FIRST_WAYPOINT_LATITUDE = 42.123
FIRST_WAYPOINT_LONGITUDE = -73.456
SECOND_WAYPOINT_LATITUDE = 42.789
SECOND_WAYPOINT_LONGITUDE = -73.987


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=duplicate-code,protected-access,redefined-outer-name


@pytest.fixture
def non_empty_commands() -> "list[dronekit.Command]":  # type: ignore
    """
    Fixture for a list of commands.
    """
    commands = [
        generate_command.waypoint(
            0.0, ACCEPT_RADIUS, FIRST_WAYPOINT_LATITUDE, FIRST_WAYPOINT_LONGITUDE, ALTITUDE
        ),
        generate_command.waypoint(
            0.0, ACCEPT_RADIUS, SECOND_WAYPOINT_LATITUDE, SECOND_WAYPOINT_LONGITUDE, ALTITUDE
        ),
    ]
    yield commands


@pytest.fixture
def empty_commands() -> "list[dronekit.Command]":  # type: ignore
    """
    Fixture for an empty list of commands.
    """
    commands = []
    yield commands


def assert_expected_takeoff_and_rtl_commands(
    commands_actual: "list[dronekit.Command]",
    commands_expected: "list[dronekit.Command]",
    altitude: float,
) -> None:
    """
    Helper function to assert the correctness of takeoff and RTL commands.
    """
    assert isinstance(commands_actual, list)

    # Test takeoff command
    takeoff_command = commands_actual[0]
    assert isinstance(takeoff_command, dronekit.Command)
    assert takeoff_command.frame == mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
    assert takeoff_command.command == mavutil.mavlink.MAV_CMD_NAV_TAKEOFF
    assert takeoff_command.z == altitude

    # Test RTL command
    rtl_command = commands_actual[-1]
    assert isinstance(rtl_command, dronekit.Command)
    assert rtl_command.frame == mavutil.mavlink.MAV_FRAME_GLOBAL
    assert rtl_command.command == mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH

    # Test original commands
    assert len(commands_actual) == len(commands_expected) + 2
    assert commands_actual[1:-1] == commands_expected


def test_add_takeoff_and_rtl_on_empty_commands(empty_commands: "list[dronekit.Command]") -> None:
    """
    Tests functionality correctness of add_takeoff_and_rtl_command on empty list of commands.
    """
    result, commands_actual = add_takeoff_and_rtl_command.add_takeoff_and_rtl_command(
        empty_commands, ALTITUDE
    )

    assert not result
    assert commands_actual is None


def test_add_takeoff_and_rtl_on_nonempty_commands(
    non_empty_commands: "list[dronekit.Command]",
) -> None:
    """
    Tests functionality correctness of add_takeoff_and_rtl_command on non-empty list of commands.
    """
    commands_expected = copy.deepcopy(non_empty_commands)
    result, commands_actual = add_takeoff_and_rtl_command.add_takeoff_and_rtl_command(
        non_empty_commands, ALTITUDE
    )

    assert result
    assert_expected_takeoff_and_rtl_commands(commands_actual, commands_expected, ALTITUDE)
