"""
Creates waypoints to avoid area bounded by verticies and rejoins path
"""

import shapely.geometry

from .common.modules import location_global


def diversion_waypoints_from_vertices(
    current_location: location_global.LocationGlobal,
    rejoin_waypoint: location_global.LocationGlobal,
    vertices: list[location_global.LocationGlobal],
) -> tuple[True, list[location_global.LocationGlobal]] | tuple[False, None]:
    """
    Finds path from current_location to rejoin_point while avoiding area bounded by vertices.

    current_location: Current location and start point of the drone.
    rejoin_waypoint: Target destination waypoint.
    vertices: Waypoints that bound a region the drone should avoid.

    Return: A list of waypoints to follow to get to the end point without flying through the restricted area.
    """

    def _calculate_waypoint_distance_squared(
        waypoint_x: location_global.LocationGlobal,
        waypoint_y: location_global.LocationGlobal,
    ) -> float:
        latitude_difference = waypoint_x.latitude - waypoint_y.latitude
        longitude_difference = waypoint_x.longitude - waypoint_y.longitude
        return latitude_difference**2 + longitude_difference**2

    diversion_waypoints: list[location_global.LocationGlobal] = [rejoin_waypoint]

    diversion_area = shapely.geometry.Polygon(
        [(vertex.latitude, vertex.longitude) for vertex in vertices]
    )

    # Dijkstra's algorithm

    # modify this buffer since units are MUCH SMALLER (long lat are by like 0.0001 differences)
    graph = [current_location, rejoin_waypoint]
    for coordinates in diversion_area.buffer(0.0001, join_style="mitre").exterior.coords:
        result, location = location_global.LocationGlobal.create(coordinates[0], coordinates[1])
        if not result:
            return False, None

        graph.append(location)

    # dist and prev indexes associated with graph
    dist: list[location_global.LocationGlobal, float] = [float("inf")] * len(graph)
    prev: list[location_global.LocationGlobal, float] = [None] * len(graph)
    queue: list[location_global.LocationGlobal] = list(graph)  # deep copy

    dist[graph.index(current_location)] = 0

    while queue:
        temp_node: location_global.LocationGlobal = min(
            queue, key=lambda node: dist[graph.index(node)]
        )

        queue.remove(temp_node)

        for node in queue:
            if shapely.geometry.LineString(
                [(temp_node.latitude, temp_node.longitude), (node.latitude, node.longitude)]
            ).intersects(diversion_area):
                continue

            temp_dist = dist[graph.index(temp_node)] + _calculate_waypoint_distance_squared(
                temp_node, node
            )

            if temp_dist < dist[graph.index(node)]:
                dist[graph.index(node)] = temp_dist
                prev[graph.index(node)] = temp_node

    temp_current = rejoin_waypoint
    while temp_current != current_location:
        temp_current = prev[graph.index(temp_current)]
        diversion_waypoints.insert(0, temp_current)

    return True, diversion_waypoints
