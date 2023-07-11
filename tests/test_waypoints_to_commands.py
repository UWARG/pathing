"""
Test process
"""

import dronekit

from modules import waypoints_to_commands


def test_waypoints_to_commands():
    waypoints = [(42.123, -73.456), (42.789, -73.987), (42.555, -73.321)]
    altitude = 100

    commands_actual = waypoints_to_commands.waypoints_to_commands(waypoints, altitude)

    assert isinstance(commands_actual, list)
    assert len(commands_actual) == len(waypoints)

    for i, command in enumerate(commands_actual):
        lat_expected = waypoints[i][0]
        lng_expected = waypoints[i][1]

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
