"""
Test process.
"""

import dronekit

from modules import waypoints_to_commands, location_ground_and_altitude
from modules.common.kml.modules import location_ground


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


def test_waypoints_to_commands_empty_input() -> None:
    """
    Tests functionality correctness of waypoints_to_commands on empty input.
    """
    waypoints = []
    altitude = 100

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
    waypoints = [
        location_ground.LocationGround("Waypoint 1", 42.123, -73.456),
        location_ground.LocationGround("Waypoint 2", 42.789, -73.987),
        location_ground.LocationGround("Waypoint 3", 42.555, -73.321),
    ]
    altitude = 100

    result, commands_actual = waypoints_to_commands.waypoints_to_commands(waypoints, altitude)

    assert result

    assert isinstance(commands_actual, list)
    assert len(commands_actual) == len(waypoints)

    for i, command in enumerate(commands_actual):
        lat_expected = waypoints[i].latitude
        lng_expected = waypoints[i].longitude

        assert isinstance(command, dronekit.Command)
        assert command.frame == dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
        assert command.command == dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
        assert command.param1 == 0
        assert command.param2 == waypoints_to_commands.ACCEPT_RADIUS
        assert command.param3 == 0
        assert command.param4 == 0
        assert command.x == lat_expected
        assert command.y == lng_expected
        assert command.z == altitude


def test_waypoints_with_altitude_to_commands() -> None:
    """
    Tests functionality correctness of waypoints_with_altitude_to commands.
    """
    waypoints = [
        location_ground_and_altitude.LocationGroundAndAltitude("Waypoint 1", 42.123, -73.456, 10.0),
        location_ground_and_altitude.LocationGroundAndAltitude("Waypoint 2", 42.789, -73.987, 20.0),
        location_ground_and_altitude.LocationGroundAndAltitude("Waypoint 3", 42.555, -73.321, 30.0),
    ]

    result, commands_actual = waypoints_to_commands.waypoints_with_altitude_to_commands(waypoints)

    assert result

    assert isinstance(commands_actual, list)
    assert len(commands_actual) == len(waypoints)

    for i, command in enumerate(commands_actual):
        lat_expected = waypoints[i].location_ground.latitude
        lng_expected = waypoints[i].location_ground.longitude
        alt_expected = waypoints[i].altitude

        assert isinstance(command, dronekit.Command)
        assert command.frame == dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
        assert command.command == dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT
        assert command.param1 == 0
        assert command.param2 == waypoints_to_commands.ACCEPT_RADIUS
        assert command.param3 == 0
        assert command.param4 == 0
        assert command.x == lat_expected
        assert command.y == lng_expected
        assert command.z == alt_expected
