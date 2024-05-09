"""
Creates waypoints to avoid area bounded by verticies and rejoins path
"""

import shapely.geometry

from .common.kml.modules import location_ground


def diversion_waypoints_from_vertices(
    current_location: location_ground.LocationGround,
    rejoin_waypoint: location_ground.LocationGround,
    verticies: "list[location_ground.LocationGround]",
) -> "list[location_ground.LocationGround]":
    """
    Finds path from current_location to rejoin_point while avoiding area bounded by verticies

    Parameters
    -----------
    current_location: "location_ground.LocationGround"
        Current location and start point of the drone
    rejoin_waypoint: location_ground.LocationGround,
        Target destination waypoint
    verticies: "list[location_ground.LocationGround]",
        Waypoints that bound a region the drone should avoid

    Returns
    -------
    list[location_ground.LocationGround]: a list of waypoints to follow to get to the end point
    without flying through the restricted area
    """

    def _calculate_waypoint_distance_squared(
        waypoint_x: location_ground.LocationGround, waypoiny_y: location_ground.LocationGround
    ) -> float:
        latitude_difference: float = waypoint_x.latitude - waypoiny_y.latitude
        longitude_difference: float = waypoint_x.longitude - waypoiny_y.longitude
        return (
            latitude_difference * latitude_difference + longitude_difference * longitude_difference
        )

    diversion_waypoints: "list[location_ground.LocationGround]" = [rejoin_waypoint]

    diversion_area: shapely.geometry.Polygon = shapely.geometry.Polygon(
        [(vertex.latitude, vertex.longitude) for vertex in verticies]
    )

    # Dijkstra's algorithm

    graph: "list[location_ground.LocationGround]" = [current_location, rejoin_waypoint] + [
        location_ground.LocationGround("", coord[0], coord[1])
        for coord in diversion_area.buffer(15, join_style="mitre").exterior.coords
    ]

    # dist and prev indexes associated with graph
    dist: "list[location_ground.LocationGround, float]" = [float("inf")] * len(graph)
    prev: "list[location_ground.LocationGround, float]" = [None] * len(graph)
    queue: "list[location_ground.LocationGround]" = list(graph)  # shallow copy

    dist[graph.index(current_location)] = 0

    while queue:
        temp_node: location_ground.LocationGround = min(
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

    temp_current: location_ground.LocationGround = rejoin_waypoint
    while temp_current != current_location:
        temp_current = prev[graph.index(temp_current)]
        diversion_waypoints.insert(0, temp_current)

    return diversion_waypoints
