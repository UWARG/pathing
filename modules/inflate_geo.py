"""Functions for manipulating polygon geometry"""

import math
import numpy as np


def get_distance(vertices_org: list, vertices_scal: list) -> list:
    """
    Given the cartesian vertices of two 2D polygon geometries (one original and one scaled), return a list where each element is the distance (in meters)
    between a vertex on the original polygon and the same vertex on the scaled polygon.
    Parameters
    -----------
    vertices_org: list
        List of vertices (latitude and longitude, in degrees) of the original polygon.
    vertices_scal: list
        List of vertices (latitude and longitude, in degrees) of the scaled polygon

    Returns
    -------
    list:
        Each element is the distance (in meters) between a vertex on the original polygon and the same vertex on the scaled polygon.
    """

    # Check for valid input
    assert len(vertices_org) == len(vertices_scal)
    assert len(vertices_org[0]) == 2 and len(vertices_scal[0]) == 2

    distances = np.zeros((len(vertices_org), 1))
    for i, (x1, y1) in enumerate(vertices_org[:-1]):
        (x2, y2) = vertices_scal[i + 1]
        (dx, dy) = (x2 - x1, y2 - y1)
        dist = math.sqrt(dx**2 + dy**2)
        distances[i] = dist

    return distances


def is_valid_polygon(vertices: list) -> bool:
    """
    Given the latlong vertices of two polygon geometries (one original and one scaled), return true if the there are not intersections between
    the edges of the vertices.

    Parameters
    -----------
    vertices: list
        List of vertices (latitude and longitude, in degrees) of the polygon.

    Returns
    -------
    bool:
        true if the there are not intersections between the edges of the vertices.
    """

    # Check for valid input:
    assert len(vertices[0]) == 2

    # Generate a list of edges joining the vertices:
    edges = np.zeros((len(vertices), 2))
    for i in range(len(edges) - 1):
        (x1, y1) = vertices[i]
        (x2, y2) = vertices[i + 1]
        (dx, dy) = (x2 - x1, y2 - y1)
        edges[i] = (dx, dy)

    # Generate the last edge (connecting last vertex in list to the first):
    (x1, y1) = vertices[len(vertices) - 1]
    (x2, y2) = vertices[0]
    (dx, dy) = (x2 - x1, y2 - y1)
    edges[len(edges) - 1] = (dx, dy)

    for i, (x1, y1) in enumerate(vertices):
        for n, (x2, y2) in enumerate(vertices):
            # Check that vertices are not the same. Skip iteration if they are.
            if np.array_equal(vertices[i], vertices[n]):
                continue
            (dx1, dy1) = edges[i]
            (dx2, dy2) = edges[n]

            # Solve for the intersection (if one exists):
            coeffs = np.array([[dx1, -dx2], [dy1, -dy2]])
            params = np.array([x2 - x1, y2 - y1])
            try:
                solution_for_intercept = np.linalg.solve(coeffs, params)
            except np.linalg.LinAlgError:
                continue

            # Use the solution to check if the intersection lies between the two vertices of the first edge:
            if i == len(vertices) - 1:
                (x3, y3) = vertices[0]
            else:
                (x3, y3) = vertices[i + 1]
            if dx1 != 0:
                solution_next_vertex = (x3 - x1) / dx1
            else:
                solution_next_vertex = (y3 - y1) / dy1

            if solution_for_intercept[0] > 0 and solution_for_intercept[0] < solution_next_vertex:
                return False

    # If all checks pass, return true:
    return True


def inflate_polygon_2d(vertices: list, scale_distance: int) -> list:
    """
    Given a list of vertices (latitude and longitude) representing a 2D polygon geometry, offset the vertices such that the perpendicular
    distance between the original and offset edges is equal to the scale distance.

    Parameters
    -----------
    vertices: list
        List of vertices (latitude and longitude, in degrees).
    scale_distance: Distance (in meters) to offset the vertices by.

    Returns
    -------
    list: List of the offset vertices (latitude and longitude, in degrees).
    """
    # Approximate distance (in meters) for one degree changes in latitude and longitude:
    deg_to_meter = 111 * (10**3)

    # Convert from latlong to cartesian:
    for i, (lat, lon) in enumerate(vertices):
        x = lat * deg_to_meter
        y = lon * deg_to_meter
        vertices[i] = (x, y)

    # Generate a list of edges joining the vertices:
    edges = np.zeros((len(vertices), 2))
    for i in range(len(edges) - 1):
        (x1, y1) = vertices[i]
        (x2, y2) = vertices[i + 1]
        (dx, dy) = (x2 - x1, y2 - y1)
        edges[i] = (dx, dy)

    # Generate the last edge (connecting last vertex in list to the first):
    (x1, y1) = vertices[len(vertices) - 1]
    (x2, y2) = vertices[0]
    (dx, dy) = (x2 - x1, y2 - y1)
    edges[len(edges) - 1] = (dx, dy)
    # For each edge, generate a perpendicular vector with a mangitude of the scaling distance:
    perp_vecs = np.zeros((len(edges), 2))
    for i, (x, y) in enumerate(edges):
        p_vec = np.array([y, -x])
        p_vec *= scale_distance / np.linalg.norm(p_vec)
        perp_vecs[i] = p_vec
    # Offset the vertices by the perpendicular vectors:
    offset_verts = np.zeros((len(edges), 2))
    for i, (x, y) in enumerate(vertices):
        (dx, dy) = perp_vecs[i]
        offset_verts[i] = np.array([x + dx, y + dy])
    # Solve for the intersections of the edges originating from the offset vertices:
    inf_verts = np.zeros((len(vertices), 2))
    for i in range(len(offset_verts) - 1):
        coeffs = np.array([[edges[i][0], -edges[i + 1][0]], [edges[i][1], -edges[i + 1][1]]])
        params = np.array(
            [
                offset_verts[i + 1][0] - offset_verts[i][0],
                offset_verts[i + 1][1] - offset_verts[i][1],
            ]
        )
        solution = np.linalg.solve(coeffs, params)
        inf_verts[i + 1] = offset_verts[i] + solution[0] * edges[i]

    # Solve for intersection of last edge to first:
    coeffs = np.array(
        [[edges[len(edges) - 1][0], -edges[0][0]], [edges[len(edges) - 1][1], -edges[0][1]]]
    )
    params = np.array(
        [
            offset_verts[0][0] - offset_verts[len(edges) - 1][0],
            offset_verts[0][1] - offset_verts[len(edges) - 1][1],
        ]
    )
    solution = np.linalg.solve(coeffs, params)
    inf_verts[0] = offset_verts[len(offset_verts) - 1] + solution[0] * edges[len(edges) - 1]

    # Perform unit tests:
    distances = get_distance(vertices, inf_verts)
    tolerance = 1
    for dist in distances:
        assert (dist - math.sqrt(2 * (scale_distance**2))) <= tolerance

    assert is_valid_polygon(inf_verts)

    # Convert cartesian to LLA:
    for i, (x, y) in enumerate(inf_verts):
        lat = x / deg_to_meter
        lon = y / deg_to_meter
        inf_verts[i] = (lat, lon)

    # Return the offset vertices:
    return inf_verts
