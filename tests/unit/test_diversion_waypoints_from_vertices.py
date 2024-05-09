"""
Test cases for creating waypoints to avoid area bounded by verticies and rejoining path
"""

import shapely.geometry

from modules import diversion_waypoints_from_vertices
from modules.common.kml.modules import location_ground

# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


def test_no_vertices_given() -> None:
    """
    Test behaviour when given no restricted area
    """
    start: location_ground.LocationGround = location_ground.LocationGround("start", 0, 0)
    end: location_ground.LocationGround = location_ground.LocationGround("end", 0, 50)
    verticies: "list[location_ground.LocationGround]" = []

    expected_path: "list[location_ground.LocationGround]" = [start, end]

    assert (
        diversion_waypoints_from_vertices.diversion_waypoints_from_vertices(start, end, verticies)
        == expected_path
    )


def test_diversion_waypoints_from_vertices() -> None:
    """
    Test correctness of diversion_waypoints_from_vertices in the normal case
    """
    start: location_ground.LocationGround = location_ground.LocationGround("start", 0, 0)
    end: location_ground.LocationGround = location_ground.LocationGround("end", 100, 0)
    verticies: "list[location_ground.LocationGround]" = [
        location_ground.LocationGround("1", 25, -25),
        location_ground.LocationGround("2", 25, 25),
        location_ground.LocationGround("3", 75, 25),
        location_ground.LocationGround("4", 75, -25),
    ]

    bounded_area: shapely.geometry.Polygon = shapely.geometry.Polygon(
        [(vertex.latitude, vertex.longitude) for vertex in verticies]
    )

    path: "list[location_ground.LocationGround]" = [start] + (
        diversion_waypoints_from_vertices.diversion_waypoints_from_vertices(start, end, verticies)
    )

    for i in range(1, len(path)):
        assert not shapely.geometry.LineString(
            [(path[i].latitude, path[i].longitude), (path[i - 1].latitude, path[i - 1].longitude)]
        ).intersects(bounded_area)


def test_concave_restricted_area():
    """
    Test correctness of diversion_waypoints_from_vertices when restricted area has concavity
    """

    start: location_ground.LocationGround = location_ground.LocationGround("start", 0, 0)
    end: location_ground.LocationGround = location_ground.LocationGround("end", 100, 0)
    verticies: "list[location_ground.LocationGround]" = [
        location_ground.LocationGround("1", 25, -25),
        location_ground.LocationGround("2", 25, 25),
        location_ground.LocationGround("3", 75, 25),
        location_ground.LocationGround("4", 50, 0),
        location_ground.LocationGround("5", 75, -25),
    ]

    bounded_area: shapely.geometry.Polygon = shapely.geometry.Polygon(
        [(vertex.latitude, vertex.longitude) for vertex in verticies]
    )

    path: "list[location_ground.LocationGround]" = [start] + (
        diversion_waypoints_from_vertices.diversion_waypoints_from_vertices(start, end, verticies)
    )

    for i in range(1, len(path)):
        assert not shapely.geometry.LineString(
            [(path[i].latitude, path[i].longitude), (path[i - 1].latitude, path[i - 1].longitude)]
        ).intersects(bounded_area)


def test_efficiency():
    """
    Test if diversion_waypoints_from_vertices produces shortest path to rejoin point
    """
    start: location_ground.LocationGround = location_ground.LocationGround("start", 0, 10)
    end: location_ground.LocationGround = location_ground.LocationGround("end", 100, 10)
    verticies: "list[location_ground.LocationGround]" = [
        location_ground.LocationGround("1", 25, -25),
        location_ground.LocationGround("2", 25, 25),
        location_ground.LocationGround("3", 75, 25),
        location_ground.LocationGround("4", 75, -25),
    ]

    path: "list[location_ground.LocationGround]" = (
        diversion_waypoints_from_vertices.diversion_waypoints_from_vertices(start, end, verticies)
    )

    for waypoint in path:
        assert waypoint.longitude > 0
