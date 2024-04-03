"""
Creates waypoints to avoid area bounded by verticies and rejoins path
"""

from .common.kml.modules import location_ground


def diversion_waypoints_from_vertices(
    current_location: "location_ground.LocationGround",
    verticies: "list[location_ground.LocationGround]",
    rejoin_waypoint: "location_ground.LocationGround",
) -> "list[location_ground.LocationGround]":

    diversion_waypoints: "list[location_ground.LocationGround]" = list()

    def _calculate_waypoint_distance_squared(
        waypoint_x: location_ground.LocationGround, waypoiny_y: location_ground.LocationGround
    ) -> float:
        latitude_difference: float = waypoint_x.latitude - waypoiny_y.latitude
        longitude_difference: float = waypoint_x.longitude - waypoiny_y.longitude
        return (
            latitude_difference * latitude_difference + longitude_difference * longitude_difference
        )

    closest_vertex_to_current_location: location_ground.LocationGround = min(
        verticies, key=lambda x: _calculate_waypoint_distance_squared(current_location, x)
    )

    closest_vertex_to_rejoin_waypoint: location_ground.LocationGround = min(
        verticies, key=lambda x: _calculate_waypoint_distance_squared(rejoin_waypoint, x)
    )

    diversion_waypoints.append(closest_vertex_to_current_location)

    cursor: int = verticies.index(closest_vertex_to_current_location)
    while verticies[cursor % len(verticies)] != closest_vertex_to_rejoin_waypoint:
        diversion_waypoints.append(verticies[cursor % len(verticies)])
        cursor += 1

    return diversion_waypoints
