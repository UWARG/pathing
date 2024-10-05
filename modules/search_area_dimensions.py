"""
Converts field of view to display dimensions in metres.
"""

from math import tan, pi


# Measurements from https://uwarg-docs.atlassian.net/wiki/spaces/CV/pages/2236613655/200+CV+Camera
FIELD_OF_VISION_X = 0.64889
FIELD_OF_VISION_Y = 0.41438


def search_area_dimensions(
    height: int,
    frustum_angle_x: float,
    frustum_angle_y: float,
    frustum_radians: bool = True,
    field_of_vision_x: float = FIELD_OF_VISION_X,
    field_of_vision_y: float = FIELD_OF_VISION_Y,
    field_of_vision_radians: bool = True,
) -> "tuple[float, float]":
    """
    Parameters:
        - height: height of the drone, in metres
        - frustum_angle_x: the left-right camera direction angle w/ respect to vertical
        - frustum_angle_y: the up-down camera direction angle w/ respect to vertical
        - frustum_radians: Boolean for whether frustum input is in radians or not
        - field_of_vision_x: the horizontal field of vision of the camera, in radians (default to measured constant)
        - field_of_vision_y: the vertical field of vision of the camera, in radians (default to measured constant)
        - field_of_vision_radians: Boolean for whether field of vision input is in radians or not

    Return:
        - tuple containing the rectangular dimensions of the field of view of the camera, in metres
    """
    frustum_factor = 1
    if not frustum_radians:
        frustum_factor = pi / 180
    field_of_vision_factor = 1
    if not field_of_vision_radians:
        field_of_vision_factor = pi / 180

    left_distance = (
        tan((field_of_vision_x * field_of_vision_factor) / 2 - frustum_angle_x * frustum_factor)
        * height
    )
    right_distance = (
        tan((field_of_vision_x * field_of_vision_factor) / 2 + frustum_angle_x * frustum_factor)
        * height
    )
    horizontal_distance = left_distance + right_distance
    up_distance = (
        tan((field_of_vision_y * field_of_vision_factor) / 2 - frustum_angle_y * frustum_factor)
        * height
    )
    down_distance = (
        tan((field_of_vision_y * field_of_vision_factor) / 2 + frustum_angle_y * frustum_factor)
        * height
    )
    vertical_distance = up_distance + down_distance
    return horizontal_distance, vertical_distance
