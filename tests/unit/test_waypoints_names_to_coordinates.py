"""
Test waypoint names to coordinates function.
"""

import pytest

from modules import waypoint_names_to_coordinates
from modules.common.modules import location_global


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


@pytest.fixture
def waypoint_dictionary() -> dict[str, location_global.LocationGlobal]:  # type: ignore
    """
    Waypoint dictionary.
    """
    name_aerial = "Aerial"
    result, location_aerial = location_global.LocationGlobal.create(9.0, 7.0)
    assert result
    assert location_aerial is not None

    name_group = "Group 15"
    result, location_group = location_global.LocationGlobal.create(3.0, 4.0)
    assert result
    assert location_group is not None

    name_robotics = "Robotics"
    result, location_robotics = location_global.LocationGlobal.create(-1.0, 0.0)
    assert result
    assert location_robotics is not None

    name_ion = "University of Waterloo Station for 301 ION"
    result, location_ion = location_global.LocationGlobal.create(6.0, 6.0)
    assert result
    assert location_ion is not None

    name_warg = "WARG"
    result, location_warg = location_global.LocationGlobal.create(8.0, 2.0)
    assert result
    assert location_warg is not None

    name_waterloo = "Waterloo"
    result, location_waterloo = location_global.LocationGlobal.create(2.0, -5.0)
    assert result
    assert location_waterloo is not None

    name_to_location_map = {
        name_aerial: location_aerial,
        name_group: location_group,
        name_robotics: location_robotics,
        name_ion: location_ion,
        name_warg: location_warg,
        name_waterloo: location_waterloo,
    }

    yield name_to_location_map


def test_valid_names(waypoint_dictionary: dict[str, location_global.LocationGlobal]) -> None:
    """
    Valid names as input.
    """
    # Setup
    names_valid = ["Waterloo", "Aerial", "Robotics", "Group 15"]
    expected = [
        waypoint_dictionary[names_valid[0]],
        waypoint_dictionary[names_valid[1]],
        waypoint_dictionary[names_valid[2]],
        waypoint_dictionary[names_valid[3]],
    ]

    # Run
    result, actual = waypoint_names_to_coordinates.waypoint_names_to_coordinates(
        names_valid,
        waypoint_dictionary,
    )

    # Test
    assert result
    assert actual == expected


def test_empty_names(waypoint_dictionary: dict[str, location_global.LocationGlobal]) -> None:
    """
    Empty list as input.
    """
    # Setup
    names_empty = []

    # Run
    result, actual = waypoint_names_to_coordinates.waypoint_names_to_coordinates(
        names_empty,
        waypoint_dictionary,
    )

    # Test
    assert not result
    assert actual is None


def test_invalid_names(waypoint_dictionary: dict[str, location_global.LocationGlobal]) -> None:
    """
    Names that don't exist in the map.
    """
    # Setup
    names_invalid = ["Hello", "World"]

    # Run
    result, actual = waypoint_names_to_coordinates.waypoint_names_to_coordinates(
        names_invalid,
        waypoint_dictionary,
    )

    # Test
    assert not result
    assert actual is None


def test_valid_and_invalid(waypoint_dictionary: dict[str, location_global.LocationGlobal]) -> None:
    """
    A mix of existent and non-existent names.
    """
    # Setup
    names_mixed = ["WARG", "Foo", "Bar"]

    # Run
    result, actual = waypoint_names_to_coordinates.waypoint_names_to_coordinates(
        names_mixed,
        waypoint_dictionary,
    )

    # Test
    assert not result
    assert actual is None
