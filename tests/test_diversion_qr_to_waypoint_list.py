"""
Testcases for parsing diversion QR code to waypoint list and a rejoin waypoint.
"""

from modules import diversion_qr_to_waypoint_list


def test_valid_multiple_avoid_waypoints():
    """
    Test valid input.
    """
    input = "Avoid the area bounded by: Alpha; Beta. Rejoin the route at Gamma"
    expected = (True, (["Alpha", "Beta"], "Gamma"))

    actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(input)

    assert actual == expected


def test_valid_single_avoid_waypoint():
    """
    Test valid input of single waypoint list and a rejoin waypoint.
    """
    input = "Avoid the area bounded by: Alpha. Rejoin the route at Beta"
    expected = (True, (["Alpha"], "Beta"))

    actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(input)

    assert actual == expected


def test_valid_waypoints_whitespace():
    """
    Test valid input with varying amounts of whitespace in between.
    """
    input = "Avoid the area bounded by: A;   B; C,;    D     . Rejoin the route at  Beta   "
    expected = (True, (["A", "B", "C,", "D"], "Beta"))

    actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(input)

    assert actual == expected
    

def test_empty_waypoint_list_and_rejoin():
    """
    Test input without waypoints list and rejoin waypoint.
    """
    input = "Avoid the area bounded by: . Rejoin the route at"
    expected = False, None

    actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(input)

    assert actual == expected


def test_empty_waypoint_list():
    """
    Test case without a waypoint list.
    """
    input = "Avoid the area bounded by: ; ;   ;   ;. Rejoin the route at Beta"
    expected = False, None

    actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(input)

    assert actual == expected


def test_empty_rejoin_waypoint():
    """
    Test case without a rejoin waypoint.
    """
    input = "Avoid the area bounded by: Zulu; Bravo; Tango; Uniform. Rejoin the route at"
    expected = False, None

    actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(input)

    assert actual == expected


def test_mismatch_input():
    """
    Test case with no matching text
    """
    input = "Lorem ipsum dolor sit amet. Zulu; Tango; Alpha."
    expected = False, None

    actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(input)

    assert actual == expected
