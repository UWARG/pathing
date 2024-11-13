"""
Testing with real files.
"""

import pathlib

import pytest

from modules import load_waypoint_name_to_coordinates_map
from modules.common.modules import location_global
from modules.common.modules import position_global_relative_altitude


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


def verify_name_to_coordinate_map(
    actual: dict[str, location_global.LocationGlobal],
    expected: dict[str, location_global.LocationGlobal],
) -> bool:
    """
    Verify dictionaries are identical.
    """
    if not len(expected) == len(actual):
        return False

    for name in actual:
        expected_location = expected[name]
        actual_location = actual[name]

        if not actual_location.latitude == pytest.approx(expected_location.latitude):
            return False

        if not actual_location.longitude == pytest.approx(expected_location.longitude):
            return False

    return True


def test_normal_file() -> None:
    """
    Normal CSV file.
    """
    # Setup
    normal_csv_file_path = pathlib.Path("tests", "test_csv", "test_normal_csv.csv")

    name_warg = "WARG"
    result, waypoint_warg = location_global.LocationGlobal.create(
        43.47323264522664, -80.54011639872981
    )
    assert result
    assert waypoint_warg is not None

    name_ion = "University of Waterloo Station for 301 ION"
    result, waypoint_ion = location_global.LocationGlobal.create(
        43.4735247614021, -80.54144667502672
    )
    assert result
    assert waypoint_ion is not None

    expected = {
        name_warg: waypoint_warg,
        name_ion: waypoint_ion,
    }

    # Run
    result, actual = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
        normal_csv_file_path,
    )

    # Test
    assert result
    assert verify_name_to_coordinate_map(actual, expected)


def test_normal_file_with_altitude() -> None:
    """
    Normal CSV file with altitude.
    """
    # Setup
    normal_csv_file_with_altitude_path = pathlib.Path(
        "tests", "test_csv", "test_normal_csv_with_altitude.csv"
    )

    name_warg = "WARG"
    result, waypoint_warg = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
        43.47323264522664, -80.54011639872981, 10.0
    )
    assert result
    assert waypoint_warg is not None

    name_ion = "University of Waterloo Station for 301 ION"
    result, waypoint_ion = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
        43.4735247614021, -80.54144667502672, 10.0
    )
    assert result
    assert waypoint_ion is not None

    expected = {
        name_warg: waypoint_warg,
        name_ion: waypoint_ion,
    }

    # Run
    (
        result,
        actual,
    ) = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_and_altitude_map(
        normal_csv_file_with_altitude_path,
    )

    # Test
    assert result
    assert verify_name_to_coordinate_map(actual, expected)


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
    (
        result,
        actual,
    ) = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_and_altitude_map(
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
    (
        result,
        actual,
    ) = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_and_altitude_map(
        nonexistent_file_path,
    )

    # Test
    assert not result
    assert actual is None
