"""
Testing with real files.
"""

import pathlib

from modules import load_waypoint_name_to_coordinates_map, location_ground_and_altitude
from modules.common.kml.modules import location_ground


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


def test_normal_file() -> None:
    """
    Normal CSV file.
    """
    # Setup
    normal_csv_file_path = pathlib.Path("tests", "test_csv", "test_normal_csv.csv")
    expected = {
        "WARG": location_ground.LocationGround("WARG", 43.47323264522664, -80.54011639872981),
        "University of Waterloo Station for 301 ION": location_ground.LocationGround(
            "University of Waterloo Station for 301 ION",
            43.4735247614021,
            -80.54144667502672,
        ),
    }

    # Run
    result, actual = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
        normal_csv_file_path,
    )

    # Test
    assert result
    assert actual == expected

def test_normal_file_with_altitude() -> None:
    """
    Normal CSV file with altitude.
    """
    # Setup
    normal_csv_file_with_altitude_path = pathlib.Path("tests", "test_csv", "test_normal_csv_with_altitude.csv")
    excepted = {
        "WARG": location_ground_and_altitude.LocationGroundAndAltitude("WARG", 43.47323264522664, -80.54011639872981, 10.0),
        "University of Waterloo Station for 301 ION": location_ground_and_altitude.LocationGroundAndAltitude(
            "University of Waterloo Station for 301 ION",
            43.4735247614021,
            -80.54144667502672,
            10.0,
        ),
    }

    # Run
    result, actual = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_and_altitude_map(
        normal_csv_file_with_altitude_path,
    )

    # Test
    assert result
    assert actual == excepted

def test_empty_file() -> None:
    """
    Empty CSV file.
    """
    # Setup
    empty_csv_file_path = pathlib.Path("test_csv", "test_empty_csv.csv")

    # Run
    result, actual = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
        empty_csv_file_path,
    )

    # Test
    assert not result
    assert actual is None

    # Run
    result, actual = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_and_altitude_map(
        empty_csv_file_path,
    )

    # Test
    assert not result
    assert actual is None


def test_nonexistent_file() -> None:
    """
    CSV file doesn't exist.
    """
    # Setup
    nonexistent_file_path = pathlib.Path("test_csv", "file_does_not_exist.abc")

    # Run
    result, actual = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
        nonexistent_file_path,
    )

    # Test
    assert not result
    assert actual is None

    # Run
    result, actual = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_and_altitude_map(
        nonexistent_file_path,
    )

    # Test
    assert not result
    assert actual is None
