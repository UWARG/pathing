"""
Module for obtaining information about the drone,
including the current waypoint sequence, location, and destination.
"""
import dronekit


def get_current_location(drone) -> "tuple[float,float]":
    """
    Function to retrieve the current location (latitude and longitude) of the drone
    """
    # Download the mission commands from the drone
    drone.commands.download()
    drone.commands.wait_ready()

    # Get the current waypoint sequence
    current_waypoint = drone.commands.next
    print(f"Current waypoint sequence: {current_waypoint}")

    # Get the current destination
    if current_waypoint < len(drone.commands):
        current_command = drone.commands[current_waypoint]
        if current_command.command == dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT:
            print(f"Current destination: Lat {current_command.x}, Lon {current_command.y}")

    # Get the current location (latitude, longitude)
    current_location = drone.location.global_frame
    if not current_location:
        return None, None

    print(f"Current location: Lat {current_location.lat}, Lon {current_location.lon}")

    return current_location.lat, current_location.lon
