"""
Test process.
"""

import dronekit

from modules import waypoints_to_spline_commands
from modules.common.kml.modules import location_ground


def test_waypoints_to_spline_commands_empty_input():
    """
    Tests functionality correctness of waypoints_to_spline_commands on empty input.
    """
    waypoints = []
    altitude = 100

    result, commands_actual = waypoints_to_spline_commands.waypoints_to_spline_commands(
        waypoints, altitude)

    assert not result
    assert commands_actual is None


def test_waypoints_to_spline_commands():
    """
    Tests functionality correctness of waypoints_to_spline_commands.
    """
    waypoints = [
        location_ground.LocationGround("Waypoint 1", 42.123, -73.456),
        location_ground.LocationGround("Waypoint 2", 42.789, -73.987),
        location_ground.LocationGround("Waypoint 3", 42.555, -73.321),
    ]
    altitude = 100

    result, commands_actual = waypoints_to_spline_commands.waypoints_to_spline_commands(
        waypoints, altitude)

    assert result

    assert isinstance(commands_actual, list)
    assert len(commands_actual) == len(waypoints)

    for i, command in enumerate(commands_actual):
        assert isinstance(command, dronekit.Command)
        assert command.frame == waypoints_to_spline_commands.MAVLINK_FRAME
        assert command.command == waypoints_to_spline_commands.MAVLINK_COMMAND
        assert command.param1 == 0
        assert command.param2 == 0
        assert command.param3 == 0
        assert command.param4 == 0
        assert command.x == waypoints[i].latitude
        assert command.y == waypoints[i].longitude
        assert command.z == altitude
