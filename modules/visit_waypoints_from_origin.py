"""
Find the optimal itinerary if we wish to distribute water from a water source to
buckets.
"""

from itertools import permutations

from haversine import haversine, Unit

from .common.modules.position_global import PositionGlobal


def waypoint_distance(point_1: PositionGlobal, point_2: PositionGlobal) -> float:
    """Return the great-circle distance of two points Earth, using Haversine's
    formula. Note that waypoints should "close" to Earth's surface (such as 500
    meters) for the formula to be accurate, because the formula ignores altitudes.

    Args:
        point_1 (PositionGlobal): First point
        point_2 (PositionGlobal): Second point

    Returns:
        float: Great-circle distance between two waypoints in meters, ignoring
            their altitudes in the calculation.
    """
    return haversine(
        (point_1.latitude, point_1.longitude),
        (point_2.latitude, point_2.longitude),
        unit=Unit.METERS,
    )


def _calculate_travel_distance(
    origin: PositionGlobal, buckets: "list[PositionGlobal]", buckets_at_once: int
) -> float:
    """Calculate the distance (in meters) by visting `buckets` in order, if you
    had to visit the origin at the start and end, and each time after visiting
    `buckets_at_once` buckets.

    Args:
        origin (PositionGlobal): The start (and end) waypoint
        buckets (list[PositionGlobal]): The buckets to visit, in order
        buckets_at_once (int): Max number of buckets to visit before
            returning to origin

    Returns:
        float: The total travel distance.
    """
    total = 0
    for i in range(0, len(buckets), buckets_at_once):
        total += waypoint_distance(origin, buckets[i])

        for j in range(i + 1, min(len(buckets), i + buckets_at_once)):
            total += waypoint_distance(buckets[j - 1], buckets[j])

        total += waypoint_distance(origin, buckets[min(len(buckets), i + buckets_at_once) - 1])

    return total


def find_optimal_path(
    origin: PositionGlobal, buckets: "list[PositionGlobal]", buckets_at_once: int = 2
) -> "list[PositionGlobal]":
    """Find an optimal itinerary of waypoints by going through all permutations
    of itineraries, given that we must
        * Visit every waypoint in `buckets`
        * Visit `origin` at the start and end of our itinerary
        * Visit `origin` each time we visit `buckets_at_once` buckets. \\

    Args:
        origin (PositionGlobal): The waypoint that we start (and end) at.
        buckets (list[PositionGlobal]): The waypoints of the buckets.
        buckets_at_once (int, optional): Maximum number of buckets that we can
            visit before returning to `origin`. Defaults to 2.

    Returns:
        list[PositionGlobal]: The list of waypoints that we visit in order,
            including `origin` at the start, end, and middle. If multiple
            optimal paths exist, return the lexicographically smallest path,
            sorted based on (latitude, longitude).
    """
    sorted_buckets = sorted(buckets, key=lambda bucket: (bucket.latitude, bucket.longitude))
    optimal_permutation = sorted_buckets
    shortest_distance = _calculate_travel_distance(origin, sorted_buckets, buckets_at_once)

    # We must permute sorted_buckets to find lexicographically smallest path,
    # sorted based on (latitude, longitude)
    for permutation in permutations(sorted_buckets):
        distance = _calculate_travel_distance(origin, permutation, buckets_at_once)

        if distance < shortest_distance:
            shortest_distance = distance
            optimal_permutation = permutation

    # the optimal permutation consists of only the buckets. We need to add the
    # origin
    path = [origin]
    for i in range(0, len(optimal_permutation), buckets_at_once):
        path.extend(optimal_permutation[i : i + buckets_at_once])
        path.append(origin)
    return path
