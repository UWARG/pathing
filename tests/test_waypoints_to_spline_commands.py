"""
Test process.
"""

import dronekit

from modules import waypoints_to_spline_commands
from modules.common.comms.modules.TelemMessages.Waypoint import Waypoint


def test_waypoints_to_commands_empty_input():
    """
    Tests functionality correctness of waypoints_to_commands on empty input.
    """
    waypoints = []
    
    result, commands_actual = waypoints_to_spline_commands.waypoints_to_spline_commands(waypoints)
    
    assert not result
    assert commands_actual is None


def test_waypoints_to_spline_commands():
    """
    Tests functionality correctness of waypoints_to_spline_commands.
    """
    waypoint_1 = Waypoint()
    waypoint_1.latitude = 42.123
    waypoint_1.longitude = -73.456
    waypoint_1.altitude = 100
    waypoint_1.waypoint_id = 1
    waypoint_2 = Waypoint()
    waypoint_2.latitude = 42.789
    waypoint_2.longitude = -73.987
    waypoint_2.altitude = 100
    waypoint_2.waypoint_id = 2
    waypoint_3 = Waypoint()
    waypoint_3.latitude = 42.555
    waypoint_3.longitude = -73.321
    waypoint_3.altitude = 100
    waypoint_3.waypoint_id = 3
    waypoints = [waypoint_1, waypoint_2, waypoint_3]

    result, commands_actual = waypoints_to_spline_commands.waypoints_to_spline_commands(waypoints)
    
    assert result

    assert isinstance(commands_actual, list)
    assert len(commands_actual) == len(waypoints)

    for i, command in enumerate(commands_actual):
        lat_expected = waypoints[i].latitude
        lng_expected = waypoints[i].longitude
        altitude_expected = waypoints[i].altitude

        assert isinstance(command, dronekit.Command)
        assert command.frame == waypoints_to_spline_commands.MAVLINK_FRAME
        assert command.command == waypoints_to_spline_commands.MAVLINK_COMMAND
        assert command.param1 == 0
        assert command.param2 == waypoints_to_spline_commands.ACCEPTANCE_RADIUS
        assert command.param3 == 0
        assert command.param4 == 0
        assert command.x == lat_expected
        assert command.y == lng_expected
        assert command.z == altitude_expected
