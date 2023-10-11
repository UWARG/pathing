"""
Testcases for parsing diversion QR code to waypoint list and a rejoin waypoint.
"""

from modules import diversion_qr_to_waypoint_list


def test_valid_multiple_avoid_waypoints():
    """
    Test valid input.
    """
    # Setup
    input = "Avoid the area bounded by: Alpha; Beta. Rejoin the route at Gamma"
    expected = ["Alpha", "Beta"], "Gamma"

    # Run
    result, actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(input)

    # Test
    assert result
    assert actual == expected


def test_valid_single_avoid_waypoint():
    """
    Test valid input of single waypoint list and a rejoin waypoint.
    """
    # Setup
    input = "Avoid the area bounded by: Alpha. Rejoin the route at Beta"
    expected = ["Alpha"], "Beta"

    # Run
    result, actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(input)

    # Test
    assert result
    assert actual == expected


def test_valid_waypoints_whitespace():
    """
    Test valid input with varying amounts of whitespace in between.
    """
    # Setup
    input = "Avoid the area bounded by: A;   B; C,;    D     . Rejoin the route at  Beta   "
    expected = ["A", "B", "C,", "D"], "Beta"

    # Run
    result, actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(input)

    # Test
    assert result
    assert actual == expected


def test_empty_waypoint_list_and_rejoin():
    """
    Test input without waypoints list and rejoin waypoint.
    """
    # Setup
    input = "Avoid the area bounded by: . Rejoin the route at"

    # Run
    result, actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(input)

    # Test
    assert not result
    assert actual is None


def test_empty_waypoint_list():
    """
    Test case without a waypoint list.
    """
    # Setup
    input = "Avoid the area bounded by: ; ;   ;   ;. Rejoin the route at Beta"

    # Run
    result, actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(input)

    # Test
    assert not result
    assert actual is None


def test_empty_rejoin_waypoint():
    """
    Test case without a rejoin waypoint.
    """
    # Setup
    input = "Avoid the area bounded by: Zulu; Bravo; Tango; Uniform. Rejoin the route at"

    # Run
    result, actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(input)

    # Test
    assert not result
    assert actual is None


def test_mismatch_input():
    """
    Test case with no matching text.
    """
    # Setup
    input = "Lorem ipsum dolor sit amet. Zulu; Tango; Alpha."

    # Run
    result, actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(input)

    # Test
    assert not result
    assert actual is None
