"""
Converts field of view from radians to metres.
"""

from math import tan, atan


FIELD_OF_VISION_X = atan(18 * (13 / 23) / 2 / 15.125) * 2
FIELD_OF_VISION_Y = atan(18 * (13 / 23) / 2 / 15.125 * (10 / 16)) * 2


def search_area_dimensions(
    height: int,
    field_of_vision_x: float = FIELD_OF_VISION_X,
    field_of_vision_y: float = FIELD_OF_VISION_Y,
) -> "tuple[float, float]":
    """
    Parameters:
        - height: height of the drone, in metres
        - field_of_vision_x: the horizontal field of vision of the camera, in radians (default to measured constant)
        - field_of_vision_y: the vertical field of vision of the camera, in radians (default to measured constant)

    Return:
        - tuple containing the rectangular dimensions of the field of view of the camera
    """
    horizontal_distance = tan(field_of_vision_x / 2) * height * 2
    vertical_distance = tan(field_of_vision_y / 2) * height * 2
    return horizontal_distance, vertical_distance
