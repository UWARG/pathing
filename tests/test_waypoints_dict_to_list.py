"""
Testing various formats of waypoints dictionary during conversion to list process.
"""

from modules import waypoints_dict_to_list


def test_valid_waypoint_dict():
    """
    Test conversion to list for a valid dict.
    """
    input =  {"Alpha": (43.4340501,-80.5789803), "Bravo": (43.4335758,-80.5775237), "Charlie": (43.4336672,-80.57839)}
    expected = [(43.4340501,-80.5789803), (43.4335758,-80.5775237), (43.4336672,-80.57839)]

    # Determine if action was successful
    result, actual = waypoints_dict_to_list.waypoints_dict_to_list(input)

    assert result
    assert actual == expected


def test_empty_waypoint_dict():
    """
    Test conversion to list for an empty dict.
    """
    input = {}

    # Determine if action was successful
    result, actual = waypoints_dict_to_list.waypoints_dict_to_list(input)

    assert not result
    assert actual is None
