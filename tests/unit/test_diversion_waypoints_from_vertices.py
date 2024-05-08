"""
Test cases for creating waypoints to avoid area bounded by verticies and rejoining path
"""

import pytest

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
    end: location_ground.LocationGround = location_ground.LocationGround("end", 0, 1)
    restricted_area: "list[location_ground.LocationGround]" = []

    expected_path: "list[location_ground.LocationGround]" = [end]

    assert (
        diversion_waypoints_from_vertices.diversion_waypoints_from_vertices(
            start, end, restricted_area
        )
        == expected_path
    )
