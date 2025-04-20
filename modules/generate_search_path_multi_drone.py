"""
Generates search path for hotspots.
"""

import math
from .common.modules import position_global_relative_altitude

CAMERA_VIEW_MARGIN = 1


def generate_search_path(
    center: position_global_relative_altitude.PositionGlobalRelativeAltitude,
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
        - A list of waypoints (PositionGlobalRelativeAltitude) if successful, or an
          empty list if the operation fails.
    """

    # Initialize the waypoints list with the starting center position
    waypoints = [center]

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
    waypoint_offset = camera_area_width / 2

    # Flag for reversing the ring of waypoints for every other loop
    direction_flag = False

    while current_radius <= search_radius:
        # Initialize angle and step size
        current_angle = 0
        angle_step = waypoint_offset / current_radius

        # waypoints for the current radius
        arc_waypoints = []

        # Generate points along the arc using while loop
        while current_angle <= angle_to_cover:
            # Apply drone's offset angle
            total_angle = current_angle + offset_angle

            # Calculate new position
            new_lat = center.latitude + current_radius * math.sin(total_angle)
            new_lon = center.longitude + current_radius * math.cos(total_angle)

            success, new_point = (
                position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
                    new_lat, new_lon, center.relative_altitude
                )
            )
            if success and new_point is not None:
                arc_waypoints.append(new_point)
            else:
                return (False, [])

            current_angle += angle_step

        # Replace the last point with the exact boundary point manually
        final_angle = angle_to_cover + offset_angle
        final_lat = center.latitude + current_radius * math.sin(final_angle)
        final_lon = center.longitude + current_radius * math.cos(final_angle)

        success, final_point = (
            position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
                final_lat, final_lon, center.relative_altitude
            )
        )
        if success and final_point is not None:
            arc_waypoints[-1] = final_point  # Replace the last point with the exact boundary point
        else:
            return (False, [])

        if direction_flag:
            arc_waypoints.reverse()

        waypoints.extend(arc_waypoints)

        direction_flag = not direction_flag
        current_radius += radius_step_size

    return (True, waypoints)
