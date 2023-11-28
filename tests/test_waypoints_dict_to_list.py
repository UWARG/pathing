"""
Testing various formats of waypoints dictionary during conversion to list process.
"""

from modules import waypoint
from modules import waypoints_dict_to_list


def test_valid_waypoint_dict():
    """
    Test conversion to list for a valid dict.
    """
    alpha = waypoint.Waypoint("Alpha", 43.4340501,-80.5789803)
    bravo = waypoint.Waypoint("Bravo", 43.4335758,-80.5775237)
    charlie = waypoint.Waypoint("Charlie", 43.4336672,-80.57839)

    waypoint_mapping = {"Alpha": alpha, "Bravo": bravo, "Charlie": charlie}
    expected = [alpha, bravo, charlie]

    # Determine if action was successful
    result, actual = waypoints_dict_to_list.waypoints_dict_to_list(waypoint_mapping)

    assert result
    assert actual == expected

def test_empty_waypoint_dict():
    """
    Test conversion to list for an empty dict.
    """
    waypoint_mapping = {}

    # Determine if action was successful
    result, actual = waypoints_dict_to_list.waypoints_dict_to_list(waypoint_mapping)

    assert not result
    assert actual is None
