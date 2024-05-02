"""
Testcases for parsing QR to waypoint.
"""

from modules import qr_to_waypoint_names


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


def test_valid_waypoint_single_simple() -> None:
    """
    Test basic single case.
    """
    text = "Follow route: Alpha"
    expected = ["Alpha"]

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(text)

    assert result
    assert actual == expected


def test_valid_waypoing_single_whitepace() -> None:
    """
    Test single waypoint with surrounding whitespace.
    """
    text = "Follow route:    Epsilon      "
    expected = ["Epsilon"]

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(text)
    assert result
    assert actual == expected


def test_valid_waypoints_multiple_simple() -> None:
    """
    Test basic case of multiple waypoints.
    """
    text = "Follow route: Waterloo; Aerial; Robotics; Group 15"
    expected = ["Waterloo", "Aerial", "Robotics", "Group 15"]

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(text)

    assert result
    assert actual == expected


def test_valid_waypoints_multiple_varying_whitespace() -> None:
    """
    Test multiple waypoints with varying amounts of whitespace in between.
    """
    text = "Follow route: A;   B; C,;    D     "
    expected = ["A", "B", "C,", "D"]

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(text)

    assert result
    assert actual == expected


def test_prefix_only() -> None:
    """
    Test text of only prefix
    """
    text = "Follow route: "
    expected = None

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(text)

    assert not result
    assert actual == expected


def test_multiple_empty_waypoints() -> None:
    """
    Test parsing of multiple empty waypoints with valid delimiter.
    """
    text = "Follow route: ; ;   ;   ;"
    expected = None

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(text)

    assert not result
    assert actual == expected


def test_invalid_waypoints_simple() -> None:
    """
    Test case where prefix string does not appear whatsoever.
    """
    text = "Avoid the area bounded by: Zulu; Bravo; Tango; Uniform.  Rejoin the route at Lima"
    expected = None

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(text)

    assert not result
    assert actual == expected


def test_invalid_waypoints_leading_whitespace() -> None:
    """
    Test case leading white space in front of otherwise valid qr string.
    """
    text = " Follow route: A; B; C; D"
    expected = None

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(text)

    assert not result
    assert actual == expected


def test_invalid_waypoints_typo() -> None:
    """
    Test incorrect capitalization/spelling of otherwise valid qr string.
    """
    text = "Follow Route: A; B; C"
    expected = None

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(text)

    assert not result
    assert actual == expected


def test_incorrect_delimiter_comma_separated() -> None:
    """
    Test valid qr string with comma delimiter.
    """
    text = "Follow route: A, B, C, D"
    expected = ["A, B, C, D"]

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(text)

    assert result
    assert actual == expected


def test_incorrect_delimiter_space_separated() -> None:
    """
    Test valid qr string with space separated waypoints.
    """
    text = "Follow route: A B C D E F G"
    expected = ["A B C D E F G"]

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(text)
    assert result
    assert actual == expected


def test_incorrect_delimiter_colon_separated() -> None:
    """
    Test valid qr string with comma separated waypoints.
    """
    text = "Follow route: A: B: C: D:"
    expected = ["A: B: C: D:"]

    result, actual = qr_to_waypoint_names.qr_to_waypoint_names(text)

    assert result
    assert actual == expected
