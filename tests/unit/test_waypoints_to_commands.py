"""
Test process.
"""

from pymavlink import mavutil

from modules import waypoints_to_commands
from modules.common.modules import location_global
from modules.common.modules import position_global_relative_altitude
from modules.common.modules.mavlink import dronekit


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name,duplicate-code


def test_waypoints_to_commands_empty_input() -> None:
    """
    Tests functionality correctness of waypoints_to_commands on empty input.
    """
    waypoints = []
    altitude = 100.0

    result, commands_actual = waypoints_to_commands.waypoints_to_commands(waypoints, altitude)

    assert not result
    assert commands_actual is None

    result, commands_actual = waypoints_to_commands.waypoints_with_altitude_to_commands(waypoints)

    assert not result
    assert commands_actual is None


def test_waypoints_to_commands() -> None:
    """
    Tests functionality correctness of waypoints_to_commands.
    """
    result, waypoint_1 = location_global.LocationGlobal.create(42.123, -73.456)
    assert result
    assert waypoint_1 is not None

    result, waypoint_2 = location_global.LocationGlobal.create(42.789, -73.987)
    assert result
    assert waypoint_2 is not None

    result, waypoint_3 = location_global.LocationGlobal.create(42.555, -73.321)
    assert result
    assert waypoint_3 is not None

    waypoints = [
        waypoint_1,
        waypoint_2,
        waypoint_3,
    ]

    altitude = 100.0

    result, commands_actual = waypoints_to_commands.waypoints_to_commands(waypoints, altitude)

    assert result

    assert isinstance(commands_actual, list)
    assert len(commands_actual) == len(waypoints)

    for i, command in enumerate(commands_actual):
        expected_latitude = waypoints[i].latitude
        expected_longitude = waypoints[i].longitude

        assert isinstance(command, dronekit.Command)
        assert command.frame == mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
        assert command.command == mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
        assert command.param1 == 0
        assert command.param2 == waypoints_to_commands.ACCEPT_RADIUS
        assert command.param3 == 0
        assert command.param4 == 0
        assert command.x == expected_latitude
        assert command.y == expected_longitude
        assert command.z == altitude


def test_waypoints_with_altitude_to_commands() -> None:
    """
    Tests functionality correctness of waypoints_with_altitude_to commands.
    """
    result, waypoint_1 = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
        42.123, -73.456, 10.0
    )
    assert result
    assert waypoint_1 is not None

    result, waypoint_2 = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
        42.789, -73.987, 20.0
    )
    assert result
    assert waypoint_2 is not None

    result, waypoint_3 = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
        42.555, -73.321, 30.0
    )
    assert result
    assert waypoint_3 is not None

    waypoints = [
        waypoint_1,
        waypoint_2,
        waypoint_3,
    ]

    result, commands_actual = waypoints_to_commands.waypoints_with_altitude_to_commands(waypoints)

    assert result

    assert isinstance(commands_actual, list)
    assert len(commands_actual) == len(waypoints)

    for i, command in enumerate(commands_actual):
        expected_latitude = waypoints[i].latitude
        expected_longitude = waypoints[i].longitude
        expected_altitude = waypoints[i].relative_altitude

        assert isinstance(command, dronekit.Command)
        assert command.frame == mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
        assert command.command == mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
        assert command.param1 == 0
        assert command.param2 == waypoints_to_commands.ACCEPT_RADIUS
        assert command.param3 == 0
        assert command.param4 == 0
        assert command.x == expected_latitude
        assert command.y == expected_longitude
        assert command.z == expected_altitude
