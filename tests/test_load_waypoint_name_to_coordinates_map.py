"""
Testing with real files.
"""

import pathlib

from modules import load_waypoint_name_to_coordinates_map
from modules import waypoint


def test_normal_file():
    """
    Normal CSV file.
    """
    # Setup
    normal_csv_file_path = pathlib.Path("tests", "test_csv", "test_normal_csv.csv")
    expected = {
        "WARG": waypoint.Waypoint("WARG", 43.47323264522664, -80.54011639872981), 
        "University of Waterloo Station for 301 ION": waypoint.Waypoint("University of Waterloo Station for 301 ION", 43.4735247614021, -80.54144667502672),
    }

    # Run
    result, actual = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
            normal_csv_file_path,
        )

    # Test
    assert result
    assert actual == expected


def test_empty_file():
    """
    Empty CSV file.
    """
    # Setup
    empty_csv_file_path = pathlib.Path("test_csv", "test_empty_csv.csv")

    # Run
    result, actual = \
        load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
            empty_csv_file_path,
        )

    # Test
    assert not result
    assert actual is None


def test_nonexistent_file():
    """
    CSV file doesn't exist.
    """
    # Setup
    nonexistent_file_path = pathlib.Path("test_csv", "file_does_not_exist.abc")

    # Run
    result, actual = \
        load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
            nonexistent_file_path,
        )

    # Test
    assert not result
    assert actual is None
