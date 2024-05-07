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

    diversion_waypoints: "list[location_ground.LocationGround]" = [
        rejoin_waypoint,
    ]

    diversion_area: shapely.geometry.Polygon = shapely.geometry.Polygon(
        [(vertex.longitude, vertex.latitude) for vertex in verticies]
    ).buffer(15, join_style="mitre")

    graph: "list[location_ground.LocationGround]" = [current_location, rejoin_waypoint] + [
        location_ground.LocationGround("", coord[0], coord[1])
        for coord in diversion_area.exterior.coords
    ]

    dist: "dict[location_ground.LocationGround, float]" = {elem: float("inf") for elem in graph}
    prev: "dict[location_ground.LocationGround, float]" = {elem: 0 for elem in graph}
    queue: "list[location_ground.LocationGround]" = graph

    dist[current_location] = 0

    while queue:
        unvisited: "list[location_ground.LocationGround]" = []
        temp_node: location_ground.LocationGround = min(
            queue, key=lambda location: location.latitude + location.longitude
        )

        for node in graph:
            if node == temp_node:
                continue
            if not shapely.geometry.LineString(
                [(temp_node.latitude, temp_node.longitude), (node.latitude, node.longitude)]
            ).intersects(diversion_area):
                unvisited.append(node)

        queue.remove(temp_node)
        for node in unvisited:
            temp_dist = dist[temp_node] + _calculate_waypoint_distance_squared(temp_node, node)
            if temp_dist < dist[node]:
                dist[node], prev[node] = temp_dist, temp_node

        temp_current: location_ground.LocationGround = rejoin_waypoint
        while temp_current != current_location:
            diversion_waypoints = prev[temp_current] + diversion_waypoints
            temp_current = prev[temp_current]

    return diversion_waypoints
