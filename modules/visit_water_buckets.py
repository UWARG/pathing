"""
Find the optimal itinerary if we wish to distribute water from a water source to
buckets.
"""

import itertools
import math

from .common.modules.position_global import PositionGlobal

# Earth radius in meters
EARTH_RADIUS = 6378137


def waypoint_distance(point_1: PositionGlobal, point_2: PositionGlobal) -> "tuple[bool, float]":
    """Return the great-circle distance of two points Earth, using Haversine's
    formula.

    Args:
        point_1 (PositionGlobal): First point
        point_2 (PositionGlobal): Second point

    Returns:
        tuple[bool, float]: Returns (False, 0) if the altitudes are different,
            and (True, distance) otherwise, where distance is the great-circle
            distance between point_1 and point_2.
    """
    # this function only calculates distance for waypoints with the same
    # altitude
    if point_1.altitude != point_2.altitude:
        return False, 0

    lat1, lon1, lat2, lon2 = map(
        math.radians,
        [
            point_1.latitude,
            point_1.longitude,
            point_2.latitude,
            point_2.longitude,
        ],
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # since the points have altitudes, the distance to the center of the earth
    # (the radius) is actually the Earth's radius plus the altitude
    radius = EARTH_RADIUS + point_1.altitude
    return True, c * radius


def _calculate_travel_distance(
    origin: PositionGlobal, buckets: "list[PositionGlobal]", buckets_at_once: int
) -> "tuple[bool, float]":
    """Calculate the distance (in meters) by visting `buckets` in order, if you
    had to visit the origin at the start and end, and each time after visiting
    `buckets_at_once` buckets.

    Args:
        origin (PositionGlobal): The start (and end) waypoint
        buckets (list[PositionGlobal]): The buckets to visit, in order
        buckets_at_once (int): Max number of buckets to visit before
            returning to origin

    Returns:
        tuple[bool, float]: Returns (False, 0) in the case of failure, otherwise
            (True, distance) where distance is the total travel distance.
    """
    total = 0
    for i in range(0, len(buckets), buckets_at_once):
        success, dist = waypoint_distance(origin, buckets[i])
        if not success:
            return False, 0
        total += dist

        for j in range(i + 1, min(len(buckets), i + buckets_at_once)):
            success, dist = waypoint_distance(buckets[j - 1], buckets[j])
            if not success:
                return False, 0
            total += dist

        success, dist = waypoint_distance(
            origin, buckets[min(len(buckets), i + buckets_at_once) - 1]
        )
        if not success:
            return False, 0
        total += dist

    return True, total


def find_optimal_path(
    origin: PositionGlobal, buckets: "list[PositionGlobal]", buckets_at_once: int = 2
) -> "tuple[bool, list[PositionGlobal]]":
    """Find an optimal itinerary of waypoints, given that we must
        * Visit every waypoint in `buckets`
        * Visit `origin` at the start and end of our itinerary
        * Visit `origin` each time we visit `buckets_at_once` buckets. \\

    Args:
        origin (PositionGlobal): The waypoint that we start (and end) at.
        buckets (list[PositionGlobal]): The waypoints of the buckets.
        buckets_at_once (int, optional): Maximum number of buckets that we can
            visit before returning to `origin`. Defaults to 2.

    Returns:
        tuple[bool, list[PositionGlobal]]: Returns (False, None) upon failure,
            otherwise (True, path) where `path` is the list of waypoints that we
            visit in order, including `origin` at the start, end, and middle.
            If multiple optimal paths exist, return the lexicographically
            smallest path based on (latitude, longitude).
    """
    sorted_buckets = sorted(
        buckets,
        key=lambda bucket: (bucket.latitude, bucket.longitude),
    )

    optimal_permutation = sorted_buckets
    success, shortest_distance = _calculate_travel_distance(origin, buckets, buckets_at_once)
    if not success:
        return False, None

    for permutation in itertools.permutations(sorted_buckets):
        success, distance = _calculate_travel_distance(origin, permutation, buckets_at_once)
        if not success:
            return False, None

        if distance < shortest_distance:
            shortest_distance = distance
            optimal_permutation = permutation

    # the optimal permutation consists of only the buckets. We need to add the
    # origin
    path = [origin]
    for i in range(0, len(optimal_permutation), buckets_at_once):
        path.extend(optimal_permutation[i : i + buckets_at_once])
        path.append(origin)
    return True, path
