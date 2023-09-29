"""
Test waypoint names to coordinates function.
"""

from modules import waypoint_names_to_coordinates
from modules.waypoint import Waypoint


WAYPOINT_DICTIONARY = {
    "Aerial": Waypoint("Aerial", 9, 7),
    "Group 15": Waypoint("Group 15", 3, 4),
    "Robotics": Waypoint("Robotics", -1, 0),
    "University of Waterloo Station for 301 ION": Waypoint("University of Waterloo Station for 301 ION", 6, 6),
    "WARG": Waypoint("WARG", 8, 2),
    "Waterloo": Waypoint("Waterloo", 2, -5),
}


def test_valid_names():
    """
    Valid names as input.
    """
    # Setup
    names_valid = ["Waterloo", "Aerial", "Robotics", "Group 15"]
    expected = [Waypoint("Waterloo", 2, -5), Waypoint("Aerial", 9, 7), Waypoint("Robotics", -1, 0), Waypoint("Group 15", 3, 4)]

    # Run
    result, actual = waypoint_names_to_coordinates.waypoint_names_to_coordinates(
        names_valid,
        WAYPOINT_DICTIONARY,
    )

    # Test
    assert result is True
    assert actual == expected


def test_empty_names():
    """
    Empty list as input.
    """
    # Setup
    names_empty = []

    # Run
    result, actual = waypoint_names_to_coordinates.waypoint_names_to_coordinates(
        names_empty,
        WAYPOINT_DICTIONARY,
    )

    # Test
    assert result is False
    assert actual is None


def test_invalid_names():
    """
    Names that don't exist in the map.
    """
    # Setup
    names_invalid = ["Hello", "World"]

    # Run
    result, actual = waypoint_names_to_coordinates.waypoint_names_to_coordinates(
        names_invalid,
        WAYPOINT_DICTIONARY,
    )

    # Test
    assert result is False
    assert actual is None


def test_valid_and_invalid():
    """
    A mix of existent and non-existent names.
    """
    # Setup
    names_mixed = ["WARG", "Foo", "Bar"]

    # Run
    result, actual = waypoint_names_to_coordinates.waypoint_names_to_coordinates(
        names_mixed,
        WAYPOINT_DICTIONARY,
    )

    # Test
    assert result is False
    assert actual is None
