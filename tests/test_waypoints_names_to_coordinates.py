"""
Test process.
"""
from modules import waypoint_names_to_coordinates

NAMES_VALID = ["Waterloo", "Aerial", "Robotics", "Group 15"]
WAYPOINT_DICTIONARY = {
    "Aerial": (9, 7),
    "Group 15": (3, 4),
    "Robotics": (-1, 0),
    "University of Waterloo Station for 301 ION": (6, 6),
    "WARG": (8, 2),
    "Waterloo": (2, -5),
}

def test_valid_names():
    NAMES_VALID = ["Waterloo", "Aerial", "Robotics", "Group 15"]
    WAYPOINT_DICTIONARY = {
        "Aerial": (9, 7),
        "Group 15": (3, 4),
        "Robotics": (-1, 0),
        "University of Waterloo Station for 301 ION": (6, 6),
        "WARG": (8, 2),
        "Waterloo": (2, -5),
    }

    result, value = waypoint_names_to_coordinates(NAMES_VALID, WAYPOINT_DICTIONARY)
    assert result is True
    assert value == [(2, -5), (9, 7), (-1, 0), (3, 4)]


def test_empty_names():
    NAMES_VALID = []
    WAYPOINT_DICTIONARY = {
        "Aerial": (9, 7),
        "Group 15": (3, 4),
        "Robotics": (-1, 0),
        "University of Waterloo Station for 301 ION": (6, 6),
        "WARG": (8, 2),
        "Waterloo": (2, -5),
    }

    result, value = waypoint_names_to_coordinates(NAMES_VALID, WAYPOINT_DICTIONARY)
    assert result is True
    assert value == []


def test_invalid_names():
    NAMES_VALID = ["WARG", "Hello", "World"]
    WAYPOINT_DICTIONARY = {
        "Aerial": (9, 7),
        "Group 15": (3, 4),
        "Robotics": (-1, 0),
        "University of Waterloo Station for 301 ION": (6, 6),
        "Waterloo": (2, -5),
    }

    result, value = waypoint_names_to_coordinates(NAMES_VALID, WAYPOINT_DICTIONARY)
    assert result is False
    assert value is None


# Run the test functions
test_valid_names()
test_empty_names()
test_invalid_names()
