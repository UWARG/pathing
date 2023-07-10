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

    for i in range(0, len(commands_actual)):
        command_actual = commands_actual[i]
        lat_expected = waypoints[i][0]
        lng_expected = waypoints[i][1]

        assert isinstance(command_actual, dronekit.Command)
        assert command_actual.frame == waypoints_to_commands.MAVLINK_FRAME
        assert command_actual.command == waypoints_to_commands.MAVLINK_COMMAND
        assert command_actual.param1 == 0
        assert command_actual.param2 == waypoints_to_commands.ACCEPT_RADIUS
        assert command_actual.param3 == 0
        assert command_actual.param4 == 0
        assert command_actual.x == lat_expected
        assert command_actual.y == lng_expected
        assert command_actual.z == altitude
