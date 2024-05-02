"""
Testcases for parsing diversion QR code to waypoint list and a rejoin waypoint.
"""

from modules import diversion_qr_to_waypoint_list


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


def test_valid_multiple_avoid_waypoints() -> None:
    """
    Test valid input.
    """
    # Setup
    text = "Avoid the area bounded by: Alpha; Beta. Rejoin the route at Gamma"
    expected = ["Alpha", "Beta"], "Gamma"

    # Run
    result, actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(text)

    # Test
    assert result
    assert actual == expected


def test_valid_single_avoid_waypoint() -> None:
    """
    Test valid input of single waypoint list and a rejoin waypoint.
    """
    # Setup
    text = "Avoid the area bounded by: Alpha. Rejoin the route at Beta"
    expected = ["Alpha"], "Beta"

    # Run
    result, actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(text)

    # Test
    assert result
    assert actual == expected


def test_valid_waypoints_whitespace() -> None:
    """
    Test valid input with varying amounts of whitespace in between.
    """
    # Setup
    text = "Avoid the area bounded by: A;   B; C,;    D     . Rejoin the route at  Beta   "
    expected = ["A", "B", "C,", "D"], "Beta"

    # Run
    result, actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(text)

    # Test
    assert result
    assert actual == expected


def test_empty_waypoint_list_and_rejoin() -> None:
    """
    Test input without waypoints list and rejoin waypoint.
    """
    # Setup
    text = "Avoid the area bounded by: . Rejoin the route at"

    # Run
    result, actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(text)

    # Test
    assert not result
    assert actual is None


def test_empty_waypoint_list() -> None:
    """
    Test case without a waypoint list.
    """
    # Setup
    text = "Avoid the area bounded by: ; ;   ;   ;. Rejoin the route at Beta"

    # Run
    result, actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(text)

    # Test
    assert not result
    assert actual is None


def test_empty_rejoin_waypoint() -> None:
    """
    Test case without a rejoin waypoint.
    """
    # Setup
    text = "Avoid the area bounded by: Zulu; Bravo; Tango; Uniform. Rejoin the route at"

    # Run
    result, actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(text)

    # Test
    assert not result
    assert actual is None


def test_mismatch_input() -> None:
    """
    Test case with no matching text.
    """
    # Setup
    text = "Lorem ipsum dolor sit amet. Zulu; Tango; Alpha."

    # Run
    result, actual = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(text)

    # Test
    assert not result
    assert actual is None
