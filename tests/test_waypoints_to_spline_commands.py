"""
Test process.
"""

import dronekit

from modules import waypoint
from modules import waypoints_to_spline_commands


def test_waypoints_to_spline_commands_empty_input():
    """
    Tests functionality correctness of waypoints_to_spline_commands on empty input.
    """
    waypoints = []
    altitude = 100

    result, commands_actual = waypoints_to_spline_commands.waypoints_to_spline_commands(waypoints, altitude)

    assert not result
    assert commands_actual is None


def test_waypoints_to_spline_commands():
    """
    Tests functionality correctness of waypoints_to_spline_commands.
    """
    waypoints = [
        waypoint.Waypoint("Waypoint 1", 42.123, -73.456),
        waypoint.Waypoint("Waypoint 2", 42.789, -73.987),
        waypoint.Waypoint("Waypoint 3", 42.555, -73.321),
    ]
    altitude = 100

    result, commands_actual = waypoints_to_spline_commands.waypoints_to_spline_commands(waypoints, altitude)

    assert result

    assert isinstance(commands_actual, list)
    assert len(commands_actual) == len(waypoints)

    for i, command in enumerate(commands_actual):
        lat_expected = waypoints[i].latitude
        lng_expected = waypoints[i].longitude

        assert isinstance(command, dronekit.Command)
        assert command.frame == waypoints_to_spline_commands.MAVLINK_FRAME
        assert command.command == waypoints_to_spline_commands.MAVLINK_COMMAND
        assert command.param1 == 0
        assert command.param2 == waypoints_to_spline_commands.ACCEPT_RADIUS
        assert command.param3 == 0
        assert command.param4 == 0
        assert command.x == lat_expected
        assert command.y == lng_expected
        assert command.z == altitude
