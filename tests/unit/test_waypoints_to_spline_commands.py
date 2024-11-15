"""
Test process.
"""

from pymavlink import mavutil

from modules import waypoints_to_spline_commands
from modules.common.modules import location_global
from modules.common.modules.mavlink import dronekit


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name,duplicate-code


def test_waypoints_to_spline_commands_empty_input() -> None:
    """
    Tests functionality of waypoints_to_spline_commands on empty input.
    """
    waypoints = []
    altitude = 100

    result, commands_actual = waypoints_to_spline_commands.waypoints_to_spline_commands(
        waypoints,
        altitude,
    )

    assert not result
    assert commands_actual is None


def test_waypoints_to_spline_commands() -> None:
    """
    Tests functionality of waypoints_to_spline_commands.
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

    altitude = 100

    result, commands_actual = waypoints_to_spline_commands.waypoints_to_spline_commands(
        waypoints,
        altitude,
    )

    assert result

    assert isinstance(commands_actual, list)
    assert len(commands_actual) == len(waypoints)

    for i, command in enumerate(commands_actual):
        assert isinstance(command, dronekit.Command)
        assert command.frame == mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
        assert command.command == mavutil.mavlink.MAV_CMD_NAV_SPLINE_WAYPOINT
        assert command.param1 == 0
        assert command.param2 == 0
        assert command.param3 == 0
        assert command.param4 == 0
        assert command.x == waypoints[i].latitude
        assert command.y == waypoints[i].longitude
        assert command.z == altitude
