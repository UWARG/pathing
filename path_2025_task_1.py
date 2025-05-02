"""
Should write located IR beacons to a kml file for task 1
File is a work in progress and should not be run yet
"""

import pathlib
import time
import yaml

from modules import add_takeoff_and_rtl_command
from modules import check_stop_condition
from modules import generate_search_path_multi_drone
from modules import upload_commands
from modules import waypoints_to_commands
from modules.common.modules.mavlink import dronekit
from modules.common.modules.position_global_relative_altitude import PositionGlobalRelativeAltitude
from modules.search_area_dimensions import search_area_dimensions

CONFIG_FILE_PATH = pathlib.Path("config.yaml")


def main() -> int:
    """
    Main function.
    """
    try:
        with CONFIG_FILE_PATH.open("r", encoding="utf8") as file:
            try:
                config = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(f"Error parsing the YAML file: {exc}")
                return -1
    except FileNotFoundError:
        print(f"File not found: {CONFIG_FILE_PATH}")
        return -1
    except IOError as exc:
        print(f"Error when opening file: {exc}")
        return -1

    # Set constants
    try:
        # pylint: disable=invalid-name
        CONNECTION_ADDRESS = config["connection_address"]
        LOG_DIRECTORY_PATH = pathlib.Path(config["log_directory_path"])
        DELAY = config["delay"]
        MAXIMUM_FLIGHT_TIME = config["maximum_flight_time"]
        result, SEARCH_CENTRE = PositionGlobalRelativeAltitude.create(
            float(config["search_centre"][0]), float(config["search_centre"][1]), 0
        )
        if not result or not SEARCH_CENTRE:
            print("ERROR: Unable to create search centre position.")
            return -1
        SEARCH_RADIUS = float(config["search_radius"])
        CAMERA_HORIZONTAL_FOV = float(config["camera"]["horizontal_fov"])
        CAMERA_VERTICAL_FOV = float(config["camera"]["vertical_fov"])
        DRONE_TIMEOUT = int(config["drone_timeout"])
        TAKEOFF_ALTITUDE = float(config["takeoff_altitude"])
        DRONE_INDEX = int(config["drones"]["index"])
        DRONE_COUNT = int(config["drones"]["count"])
        # pylint: enable=invalid-name
    except KeyError as exc:
        print(f"Unable to find key in yaml file: {exc}")
        return -1

    pathlib.Path(LOG_DIRECTORY_PATH).mkdir(exist_ok=True)

    # Wait ready is false as the drone may be on the ground
    drone = dronekit.connect(CONNECTION_ADDRESS, wait_ready=False)

    # Calculate the drone's visible dimensions on the ground, in meters
    visible_horizontal_length, visible_vertical_length = search_area_dimensions(
        TAKEOFF_ALTITUDE, 0, 0, True, CAMERA_HORIZONTAL_FOV, CAMERA_VERTICAL_FOV, False
    )

    # Generate itinerary to find hotspots
    result, waypoints = generate_search_path_multi_drone.generate_search_path(
        centre=SEARCH_CENTRE,
        search_radius=SEARCH_RADIUS,
        camera_area_dimensions=(visible_horizontal_length, visible_vertical_length),
        drone_index=DRONE_INDEX,
        drone_count=DRONE_COUNT,
    )
    if not result or not waypoints:
        print("ERROR: Generating search path failed.")
        return -1

    result, waypoint_commands = waypoints_to_commands.waypoints_with_altitude_to_commands(waypoints)
    if not result or not waypoint_commands:
        print("ERROR: Converting waypoints to commands failed.")
        return -1

    result, takeoff_rtl_commands = add_takeoff_and_rtl_command.add_takeoff_and_rtl_command(
        waypoint_commands, TAKEOFF_ALTITUDE
    )
    if not result or not takeoff_rtl_commands:
        print("ERROR: Adding takeoff/RTL commands failed.")
        return -1

    result = upload_commands.upload_commands(drone, takeoff_rtl_commands, DRONE_TIMEOUT)
    if not result:
        print("ERROR: Uploading drone commands failed.")
        return -1

    start_time = time.time()
    while True:
        # Send drone back to launch if we exceed max flight time
        current_time = time.time()
        is_returning_to_launch = check_stop_condition.check_stop_condition(
            start_time, current_time, drone, MAXIMUM_FLIGHT_TIME
        )

        if is_returning_to_launch:
            break

        print(f"Elapsed time(s): {current_time - start_time}")
        time.sleep(DELAY)

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main != 0:
        print(f"ERROR: Status Code: {result_main}")

    print("Done!")
