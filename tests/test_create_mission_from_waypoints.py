"""
Test process for the create_mission_from_waypoints module
"""

import pytest

from modules import create_mission_from_waypoints
from modules.common.kml.modules import location_ground


TAKEOFF_ALTITUDE = 100
LAPS_ALTITUDE = 50
NUM_LAPS = 2


@pytest.fixture
def non_empty_start_sequence() -> "list[location_ground.LocationGround]":
    takeoff_sequence = [
        location_ground.LocationGround("Alpha", 48.5112750, -71.6505486),
    ]
    yield takeoff_sequence


@pytest.fixture
def non_empty_lap_sequence() -> "list[location_ground.LocationGround]":
    lap_sequence = [
        location_ground.LocationGround("waypoint 1", 43.4363951, -80.5861617),
        location_ground.LocationGround("waypoint 2", 43.4335848, -80.5767288),
        location_ground.LocationGround("waypoint 3", 43.4338880, -80.5764634),
        location_ground.LocationGround("waypoint 4", 43.4366668, -80.5859371),
    ]
    yield lap_sequence


def test_no_laps(
    non_empty_start_sequence: "list[location_ground.LocationGround]",
    non_empty_lap_sequence: "list[location_ground.LocationGround]",
):
    """
    Tests for correct functionality when we pass in no laps
    """
    success, mission = create_mission_from_waypoints.create_mission_from_waypoints(
        0,
        TAKEOFF_ALTITUDE,
        LAPS_ALTITUDE,
        non_empty_start_sequence,
        non_empty_lap_sequence,
    )
    assert not success
    assert mission is None


def test_empty_start_sequence(
    non_empty_lap_sequence: "list[location_ground.LocationGround]",
):
    """
    Tests functionaltiy for an empty start sequence
    """
    start_sequence = []
    success, mission = create_mission_from_waypoints.create_mission_from_waypoints(
        NUM_LAPS,
        TAKEOFF_ALTITUDE,
        LAPS_ALTITUDE,
        start_sequence,
        non_empty_lap_sequence,
    )
    assert not success
    assert mission is None


def test_empty_lap_sequence(
    non_empty_start_sequence: "list[location_ground.LocationGround]",
):
    """
    Tests functionaltiy for an empty lap sequence
    """
    lap_sequence = []
    success, mission = create_mission_from_waypoints.create_mission_from_waypoints(
        NUM_LAPS,
        TAKEOFF_ALTITUDE,
        LAPS_ALTITUDE,
        non_empty_start_sequence,
        lap_sequence,
    )
    assert not success
    assert mission is None


def test_valid_waypoints(
    non_empty_start_sequence: "list[location_ground.LocationGround]",
    non_empty_lap_sequence: "list[location_ground.LocationGround]",
):
    """
    Ensures that mission is correctly made based on valid parameters
    """
    print("Todo")
    success, mission_actual = create_mission_from_waypoints.create_mission_from_waypoints(
        NUM_LAPS,
        TAKEOFF_ALTITUDE,
        LAPS_ALTITUDE,
        non_empty_start_sequence,
        non_empty_lap_sequence,
    )
    assert success
    assert isinstance(mission_actual, list)
    assert len(mission_actual) == (
        len(non_empty_start_sequence) + NUM_LAPS * len(non_empty_lap_sequence)
    )

    # list of the expected waypoints, making sure they mapped correctly
    expected_list = non_empty_start_sequence + NUM_LAPS * non_empty_lap_sequence
    for index, waypoint_command in enumerate(mission_actual):
        if index < len(non_empty_start_sequence):
            assert waypoint_command.z == TAKEOFF_ALTITUDE
        else:
            assert waypoint_command.z == LAPS_ALTITUDE

        assert waypoint_command.x == expected_list[index].latitude
        assert waypoint_command.y == expected_list[index].longitude
