"""
Test process
"""
import dronekit

from modules.waypoints_to_commands import waypoints_to_commands, ACCEPT_RADIUS


def test_waypoints_to_commands():
    mock_waypoints_data = [(42.123, -73.456), (42.789, -73.987), (42.555, -73.321)]
    mock_altitude_data = 100

    commands = waypoints_to_commands(mock_waypoints_data, mock_altitude_data)

    assert isinstance(commands, list)
    assert len(commands) == len(mock_waypoints_data)

    for command in commands:
        assert isinstance(command, dronekit.Command)
        assert command.frame == dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
        assert command.command == dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
        assert command.param1 == 0
        assert command.param2 == ACCEPT_RADIUS
        assert command.param3 == 0
        assert command.param4 == 0
        assert command.x == mock_waypoints_data[commands.index(command)][0]
        assert command.y == mock_waypoints_data[commands.index(command)][1]
        assert command.z == mock_altitude_data
