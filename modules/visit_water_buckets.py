"""
Find the optimal itinerary if we wish to distribute water from a water source to
buckets.
"""

import itertools

from .waypoint import Waypoint
from .waypoint import waypoint_distance


def _calculate_travel_distance(
    origin: Waypoint, buckets: "list[Waypoint]", buckets_at_once: int
) -> "tuple[bool, float]":
    """Calculate the distance (in meters) by visting `buckets` in order, if you
    had to visit the origin at the start and end, and each time after visiting
    `buckets_at_once` buckets.

    Args:
        origin (Waypoint): The start (and end) waypoint
        buckets (list[Waypoint]): The buckets to visit, in order
        buckets_at_once (_type_): Max number of buckets to visit before
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
    origin: Waypoint, buckets: "list[Waypoint]", buckets_at_once: int = 2
) -> "tuple[bool, list[Waypoint]]":
    """Find an optimal itinerary of waypoints, given that we must
        * Visit every waypoint in `buckets`
        * Visit `origin` at the start and end of our itinerary
        * Visit `origin` each time we visit `buckets_at_once` buckets. \\

    Args:
        origin (Waypoint): The waypoint that we start (and end) at.
        buckets (list[Waypoint]): The waypoints of the buckets.
        buckets_at_once (int, optional): Maximum number of buckets that we can
            visit before returning to `origin`. Defaults to 2.

    Returns:
        tuple[bool, list[Waypoint]]: Returns (False, None) upon failure,
            otherwise (True, path) where `path` is the list of waypoints that we
            visit in order, including `origin` at the start, end, and middle.
            If multiple optimal paths exist, return the lexicographically
            smallest path based on (latitude, longitude).
    """
    sorted_buckets = sorted(
        buckets,
        key=lambda bucket: (bucket.location_ground.latitude, bucket.location_ground.longitude),
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
