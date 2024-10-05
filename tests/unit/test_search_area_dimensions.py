"""
Test cases for the search_area_dimensions module.
"""

from math import pi, sqrt

from ...modules import search_area_dimensions

# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=duplicate-code,protected-access,redefined-outer-name

THRESHOLD = 1e-6


def test_no_field_of_view() -> None:
    """
    Testing 0 degree field of view.
    """
    height = 10
    frustum_angle_x = 10
    frustum_angle_y = 20
    field_of_vision_x = 0
    field_of_vision_y = 0

    x, y = search_area_dimensions.search_area_dimensions(
        height, frustum_angle_x, frustum_angle_y, True, field_of_vision_x, field_of_vision_y, True
    )

    assert abs(x - 0) < THRESHOLD
    assert abs(y - 0) < THRESHOLD


def test_vertical_field_of_view() -> None:
    """
    Testing straight-down camera angle.
    """
    height = 20
    frustum_angle_x = 0
    frustum_angle_y = 0
    field_of_vision_x = pi / 2
    field_of_vision_y = 2 * pi / 3

    x, y = search_area_dimensions.search_area_dimensions(
        height, frustum_angle_x, frustum_angle_y, True, field_of_vision_x, field_of_vision_y, True
    )

    assert abs(x - 40) < THRESHOLD
    assert abs(y - 40 * sqrt(3)) < THRESHOLD


def test_side_vertical_field_of_view() -> None:
    """
    Test for when one side of the field of view is vertical.
    """
    height = 30
    frustum_angle_x = pi / 8
    frustum_angle_y = pi / 6
    field_of_vision_x = pi / 4
    field_of_vision_y = pi / 3

    x, y = search_area_dimensions.search_area_dimensions(
        height, frustum_angle_x, frustum_angle_y, True, field_of_vision_x, field_of_vision_y, True
    )

    assert abs(x - 30) < THRESHOLD
    assert abs(y - 30 * sqrt(3)) < THRESHOLD


def test_askew_acute_field_of_view() -> None:
    """
    Test for when field of view spreads outwards on both sides.
    """
    height = 40
    frustum_angle_x = pi / 12
    frustum_angle_y = pi / 24
    field_of_vision_x = pi / 2
    field_of_vision_y = 7 * pi / 12

    x, y = search_area_dimensions.search_area_dimensions(
        height, frustum_angle_x, frustum_angle_y, True, field_of_vision_x, field_of_vision_y, True
    )

    assert abs(x - (40 * sqrt(3) + 40 / sqrt(3))) < THRESHOLD
    assert abs(y - (40 + 40 * sqrt(3))) < THRESHOLD


def test_askew_obtuse_field_of_view() -> None:
    """
    Test for when field of view spreads to one side from both directions.
    """
    height = 50
    frustum_angle_x = pi / 4
    frustum_angle_y = 7 * pi / 24
    field_of_vision_x = pi / 6
    field_of_vision_y = pi / 12

    x, y = search_area_dimensions.search_area_dimensions(
        height, frustum_angle_x, frustum_angle_y, True, field_of_vision_x, field_of_vision_y, True
    )

    assert abs(x - (50 * sqrt(3) - 50 / sqrt(3))) < THRESHOLD
    assert abs(y - (50 * sqrt(3) - 50)) < THRESHOLD
