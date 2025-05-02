"""
Generates search path for hotspots.
"""

import math
from .common.modules import position_global_relative_altitude

CAMERA_VIEW_MARGIN = 1
METERS_PER_LAT = 111319.9  # Meters per degree of latitude
ARC_RESOLUTION = 5  # Lower is better


def generate_search_path(
    centre: position_global_relative_altitude.PositionGlobalRelativeAltitude,
    search_radius: float,
    camera_area_dimensions: tuple[float, float],
    drone_index: int,
    drone_count: int,
) -> tuple[bool, list[position_global_relative_altitude.PositionGlobalRelativeAltitude]]:
    """
    Generate a search path for a single drone in a multi-drone system.

    The function divides a circular search area into equal sectors, with each drone
    assigned one sector. It generates waypoints for the drone to follow along an arc
    within its assigned sector, ensuring even coverage of the area.

    center: The center of the circular search area.
    search_radius: The maximum radius of the search area, in meters.
    camera_area_dimensions: A tuple (width, height) representing the dimensions of the camera's field of view, in meters.
    drone_index: The index of the drone (0-based) in the multi-drone system.
    drone_count: The total number of drones in the system.

    Return: A tuple containing:
        - A boolean indicating success (True) or failure (False).
        - A list of waypoints (PositionGlobalRelativeAltitude) if succescentresful, or an
          empty list if the operation fails.
    """
    meters_per_lon = METERS_PER_LAT * math.cos(math.radians(centre.latitude))

    # Initialize the waypoints list with the starting center position
    waypoints = []

    # Extract camera area dimensions and adjust for the margin
    camera_area_width, camera_area_height = camera_area_dimensions
    camera_area_width -= CAMERA_VIEW_MARGIN
    camera_area_height -= CAMERA_VIEW_MARGIN

    # Calculate the angle each drone needs to cover and the offset for this drone
    angle_to_cover = 2 * math.pi / drone_count
    offset_angle = drone_index * angle_to_cover

    # Determine the step size for the radius and initialize the current radius
    radius_step_size = camera_area_width / 2
    current_radius = radius_step_size

    # Define the offset for waypoints along the arc
    waypoint_offset = camera_area_height

    # Flag for reversing the ring of waypoints for every other loop
    direction_flag = False

    while current_radius < search_radius + radius_step_size:
        # clamp radius to search radius
        current_radius = min(current_radius, search_radius)

        # Initialize angle and step size
        current_angle = 0
        angle_step = ARC_RESOLUTION * math.asin(waypoint_offset / (2 * current_radius))

        # waypoints for the current radius
        arc_waypoints = []

        # Generate points along the arc using while loop
        while current_angle < angle_to_cover + angle_step:
            # clamp angle to angle to cover
            current_angle = min(current_angle, angle_to_cover)

            # Apply drone's offset angle
            total_angle = current_angle + offset_angle

            # Calculate new position
            new_lat = centre.latitude + (current_radius * math.sin(total_angle)) / METERS_PER_LAT
            new_lon = centre.longitude + (current_radius * math.cos(total_angle)) / meters_per_lon

            success, new_point = (
                position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
                    new_lat, new_lon, centre.relative_altitude
                )
            )
            if success and new_point is not None:
                arc_waypoints.append(new_point)
            else:
                return (False, [])

            current_angle += angle_step

        if direction_flag:
            arc_waypoints.reverse()

        waypoints.extend(arc_waypoints)

        direction_flag = not direction_flag
        current_radius += radius_step_size

    return (True, waypoints)
