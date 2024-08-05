"""Functions for manipulating polygon geometry"""

import math
import numpy as np


def inflate_convex_polygon(vertices: np.ndarray, scale_distance: int) -> np.ndarray:
    """
    Given a list of vertices representing a convex polygon geometry, offset the vertices such that the perpendicular
    distance between the original and offset edges is equal to the scale distance.

    Parameters
    -----------
    vertices: np.ndarray
        List of vertices
    scale_distance: Distance (in meters) to offset the vertices by

    Returns
    -------
    np.ndarray: List of the offset vertices
    """
    # Referance radius for altitude (Radius of earth = 6371 km):
    r_ref = 6371 * (10**3)

    # Convert LLA coordinates from degrees to radians:
    for i, (lat, lon, alt) in enumerate(vertices):
        lat_deg, lon_deg = math.radians(lat), math.radians(lon)
        vertices[i] = (lat_deg, lon_deg, alt)

    # Convert to LLA to cartesian:
    for i, (lat, lon, alt) in enumerate(vertices):
        x = (r_ref + alt) * math.cos(lat) * math.cos(lon)
        y = (r_ref + alt) * math.cos(lat) * math.sin(lon)
        z = (r_ref + alt) * math.sin(lat)
        vertices[i] = (x, y, z)

    # Generate a list of edges joining the vertices:
    edges = np.zeros((len(vertices), 3))
    for i in range(len(edges) - 1):
        (x1, y1, z1) = vertices[i]
        (x2, y2, z2) = vertices[i + 1]
        (dx, dy, dz) = (x2 - x1, y2 - y1, z2 - z1)
        edges[i] = (dx, dy, dz)

    # Generate the last edge (connecting last vertex in list to the first).
    (x1, y1, z1) = vertices[len(vertices) - 1]
    (x2, y2, z2) = vertices[0]
    (dx, dy, dz) = (x2 - x1, y2 - y1, z2 - z1)
    edges[len(edges) - 1] = (dx, dy, dz)

    # Calculate the direction vector of the angle bisectors:
    bisectors = np.zeros((len(edges), 3))
    for i in range(len(bisectors) - 1):
        edge1 = np.array(edges[i])
        edge2 = np.array(edges[i + 1])
        edge1 = edge1 / np.linalg.norm(edge1)
        edge2 = edge2 / np.linalg.norm(edge2)
        bisector = edge1 + edge2
        bisector /= np.linalg.norm(bisector)

        # Calculate the required norm of the bisector vector given the scaling factor
        l = scale_distance / math.sqrt((1 + np.dot(edge1, edge2)) / 2)
        bisector *= l
        bisectors[i] = bisector

    # Calculate final bisector (final edge with first)
    edge1 = np.array(edges[len(edges) - 1])
    edge2 = np.array(edges[0])
    edge1 = edge1 / np.linalg.norm(edge1)
    edge2 = edge2 / np.linalg.norm(edge2)
    bisector = edge1 + edge2
    bisector /= np.linalg.norm(bisector)

    # Calculate the required norm of the bisector vector given the scaling factor
    l = scale_distance / math.sqrt((1 + np.dot(edge1, edge2)) / 2)
    bisector *= l
    bisectors[len(bisectors) - 1] = bisector

    # Offset the vertices by the bisector vectors
    offset_verts = np.zeros((len(edges), 3))
    for i, ((x1, y1, z1), (x2, y2, z2)) in enumerate(zip(vertices, bisectors)):
        offset_verts[i] = (x1 - x2, y1 - y2, z1 - z2)

    # Convert cartesian to LLA
    for i, (x, y, z) in enumerate(offset_verts):
        (x, y, z) = offset_verts[i]
        lon = math.atan2(y, x)
        lat = math.atan2(z, x)
        alt = math.sqrt(x**2 + y**2 + z**2) - r_ref

        # Convert lat and long from radians to degrees
        lon = math.degrees(lon)
        lat = math.degrees(lat)

        offset_verts[i] = lat, lon, alt

    # Return the offset vertices
    return offset_verts


triangle = np.array(
    [[48.8567, 2.3508, 0], [61.4140105652, 23.7281341313, 0], [51.760597, -1.261247, 0]]
)
print(inflate_convex_polygon(triangle, 5))
