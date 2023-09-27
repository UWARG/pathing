"""
Test process.
"""

import dronekit

from modules.waypoint import Waypoint
from modules import waypoints_to_commands


def test_waypoints_to_commands_empty_input():
    """
    Tests functionality correctness of waypoints_to_commands on empty input.
    """
    waypoints = []
    altitude = 100
    
    result, commands_actual = waypoints_to_commands.waypoints_to_commands(waypoints, altitude)
    
    assert not result
    assert commands_actual is None


def test_waypoints_to_commands():
    """
    Tests functionality correctness of waypoints_to_commands.
    """
    waypoints = [Waypoint("Waypoint 1", 42.123, -73.456), Waypoint("Waypoint 2", 42.789, -73.987), Waypoint("Waypoint 3", 42.555, -73.321)]
    altitude = 100

    result, commands_actual = waypoints_to_commands.waypoints_to_commands(waypoints, altitude)
    
    assert result

    assert isinstance(commands_actual, list)
    assert len(commands_actual) == len(waypoints)

    for i, command in enumerate(commands_actual):
        lat_expected = waypoints[i].latitude
        lng_expected = waypoints[i].longitude

        assert isinstance(command, dronekit.Command)
        assert command.frame == waypoints_to_commands.MAVLINK_FRAME
        assert command.command == waypoints_to_commands.MAVLINK_COMMAND
        assert command.param1 == 0
        assert command.param2 == waypoints_to_commands.ACCEPT_RADIUS
        assert command.param3 == 0
        assert command.param4 == 0
        assert command.x == lat_expected
        assert command.y == lng_expected
        assert command.z == altitude
