"""
Converts field of view from radians to metres.
"""

from math import tan, atan


FIELD_OF_VISION_X = atan(18 * (13 / 23) / 2 / 15.125) * 2
FIELD_OF_VISION_Y = atan(18 * (13 / 23) / 2 / 15.125 * (10 / 16)) * 2


def search_area_dimensions(
    height: int,
    frustum_angle_x: float,
    frustum_angle_y: float,
    field_of_vision_x: float = FIELD_OF_VISION_X,
    field_of_vision_y: float = FIELD_OF_VISION_Y,
) -> "tuple[float, float]":
    """
    Parameters:
        - height: height of the drone, in metres
        - frustum_angle_x: the left-right camera direction angle w/ respect to vertical
        - frustum_angle_y: the up-down camera direction angle w/ respect to vertical
        - field_of_vision_x: the horizontal field of vision of the camera, in radians (default to measured constant)
        - field_of_vision_y: the vertical field of vision of the camera, in radians (default to measured constant)

    Return:
        - tuple containing the rectangular dimensions of the field of view of the camera
    """
    left_distance = tan((field_of_vision_x) / 2 - frustum_angle_x) * height
    right_distance = tan((field_of_vision_x) / 2 + frustum_angle_x) * height
    horizontal_distance = left_distance + right_distance
    up_distance = tan((field_of_vision_y) / 2 - frustum_angle_y) * height
    down_distance = tan((field_of_vision_y) / 2 + frustum_angle_y) * height
    vertical_distance = up_distance + down_distance
    return horizontal_distance, vertical_distance
