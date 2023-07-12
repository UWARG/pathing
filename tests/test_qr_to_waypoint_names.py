"""
Testcases for parsing QR to waypoint.
"""

from modules import qr_to_waypoint_names


def test_valid_waypoint_single_simple():
    """
    Test basic single case.
    """
    input = "Follow route: Alpha"
    expected = ["Alpha"]

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(input)

    assert result
    assert actual == expected


def test_valid_waypoing_single_whitepace():
    """
    Test single waypoint with surrounding whitespace.
    """
    input = "Follow route:    Epsilon      "
    expected = ["Epsilon"]

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(input)
    assert result
    assert actual == expected


def test_valid_waypoints_multiple_simple():
    """
    Test basic case of multiple waypoints.
    """
    input = "Follow route: Waterloo; Aerial; Robotics; Group 15"
    expected = ["Waterloo", "Aerial", "Robotics", "Group 15"]

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(input)

    assert result
    assert actual == expected


def test_valid_waypoints_multiple_varying_whitespace():
    """
    Test multiple waypoints with varying amounts of whitespace in between.
    """
    input = "Follow route: A;   B; C,;    D     "
    expected = ["A", "B", "C,", "D"]

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(input)

    assert result
    assert actual == expected
    

def test_prefix_only():
    """
    Test input of only prefix
    """
    input = "Follow route: "
    expected = None

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(input)

    assert not result
    assert actual == expected


def test_multiple_empty_waypoints():
    """
    Test parsing of multiple empty waypoints with valid delimiter.
    """
    input = "Follow route: ; ;   ;   ;"
    expected = None

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(input)

    assert not result
    assert actual == expected


def test_invalid_waypoints_simple():
    """
    Test case where prefix string does not appear whatsoever.
    """
    input = "Avoid the area bounded by: Zulu; Bravo; Tango; Uniform.  Rejoin the route at Lima"
    expected = None

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(input)

    assert not result
    assert actual == expected


def test_invalid_waypoints_leading_whitespace():
    """
    Test case leading white space in front of otherwise valid qr string.
    """
    input = " Follow route: A; B; C; D"
    expected = None

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(input)

    assert not result
    assert actual == expected


def test_invalid_waypoints_typo():
    """
    Test incorrect capitalization/spelling of otherwise valid qr string.
    """
    input = "Follow Route: A; B; C"
    expected = None

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(input)

    assert not result
    assert actual == expected


def test_incorrect_delimiter_comma_separated():
    """
    Test valid qr string with comma delimiter.
    """
    input = "Follow route: A, B, C, D"
    expected = ["A, B, C, D"]

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(input)

    assert result
    assert actual == expected


def test_incorrect_delimiter_space_separated():
    """
    Test valid qr string with space separated waypoints.
    """
    input = "Follow route: A B C D E F G"
    expected = ["A B C D E F G"]

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(input)
    assert result
    assert actual == expected


def test_incorrect_delimiter_colon_separated():
    """
    Test valid qr string with comma separated waypoints.
    """
    input = "Follow route: A: B: C: D:"
    expected = ["A: B: C: D:"] 

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names("Follow route: A: B: C: D:")

    assert result
    assert actual == expected
