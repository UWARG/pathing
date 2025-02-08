"""
Test finding great-circle distance between two waypoints.
"""

from modules.common.modules.position_global import PositionGlobal
from modules.visit_water_buckets import waypoint_distance


def test_waypoint_distance() -> None:
    """
    Test distance between two points, 319.40 meters apart.
    """
    point_1 = PositionGlobal.create(43.469880, -80.534243, 1)[1]
    point_2 = PositionGlobal.create(43.469984, -80.538194, 1)[1]

    success, distance = waypoint_distance(point_1, point_2)
    assert success
    assert abs(distance - 319.40) < 0.01
