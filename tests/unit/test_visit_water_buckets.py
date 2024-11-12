"""
Test finding optimal itinerary of waypoints to visit.
"""

from modules.visit_water_buckets import find_optimal_path
from modules.waypoint import Waypoint


def test_2_buckets_at_once() -> None:
    """
    Test visiting at most 2 buckets at once.
    """
    origin = Waypoint("Origin", 43.47073179293396, -80.53501978862127, 1)  # UWP Beck Hall
    buckets = [
        Waypoint("Bucket 0", 43.46925477790072, -80.54034107786745, 1),  # SCH
        Waypoint("Bucket 1", 43.46834804571286, -80.54341048064786, 1),  # E3
        Waypoint("Bucket 2", 43.46983001550084, -80.54225704095209, 1),  # DP
        Waypoint("Bucket 3", 43.47153126326250, -80.54211697668684, 1),  # EIT
        Waypoint("Bucket 4", 43.47076658531946, -80.54311788821606, 1),  # STC
    ]

    success, path = find_optimal_path(origin, buckets, 2)
    assert success
    assert path == [
        origin,
        buckets[4],
        buckets[3],
        origin,
        buckets[2],
        buckets[1],
        origin,
        buckets[0],
        origin,
    ]


def test_3_buckets_at_once() -> None:
    """
    Test visiting at most 3 buckets at once.
    """
    origin = Waypoint("Origin", 43.47073179293396, -80.53501978862127, 1)  # UWP Beck Hall
    buckets = [
        Waypoint("Bucket 0", 43.46925477790072, -80.54034107786745, 1),  # SCH
        Waypoint("Bucket 1", 43.46834804571286, -80.54341048064786, 1),  # E3
        Waypoint("Bucket 2", 43.46983001550084, -80.54225704095209, 1),  # DP
        Waypoint("Bucket 3", 43.47153126326250, -80.54211697668684, 1),  # EIT
        Waypoint("Bucket 4", 43.47076658531946, -80.54311788821606, 1),  # STC
    ]

    success, path = find_optimal_path(origin, buckets, 3)
    assert success
    assert path == [
        origin,
        buckets[0],
        buckets[1],
        buckets[2],
        origin,
        buckets[4],
        buckets[3],
        origin,
    ]
