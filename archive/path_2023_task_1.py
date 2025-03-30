"""
Reads waypoints from QR code and sends drone commands.
"""

import pathlib
import time
import msvcrt

import dronekit

from modules import add_takeoff_and_landing_command
from modules import load_waypoint_name_to_coordinates_map
from modules import upload_commands
from modules import waypoint_tracking
from modules import waypoints_dict_to_list
from modules import waypoints_to_commands
from modules import diversion_waypoints_from_vertices
from modules import generate_command
from modules.common.modules import location_global


WAYPOINT_FILE_PATH = pathlib.Path("2023", "waypoints", "competition_task_1.csv")
DIVERSION_WAYPOINT_FILE_PATH = pathlib.Path("2023", "waypoints", "diversion_waypoints.csv")
REJOIN_WAYPOINT_FILE_PATH = pathlib.Path("2023", "waypoints", "rejoin_waypoint.csv")
CAMERA = 0
ALTITUDE = 40
DRONE_TIMEOUT = 30.0  # seconds
CONNECTION_ADDRESS = "tcp:localhost:14550"
LOG_DIRECTORY_PATH = pathlib.Path("logs")
KML_FILE_PREFIX = "waypoints"
DELAY = 0.1  # seconds


# Code copied into path_2024.py
# pylint: disable=duplicate-code
def main() -> int:
    """
    Main function.
    """
    pathlib.Path(LOG_DIRECTORY_PATH).mkdir(exist_ok=True)

    # Wait ready is false as the drone may be on the ground
    drone = dronekit.connect(CONNECTION_ADDRESS, wait_ready=False)

    # Read in hardcoded waypoints from CSV file
    # Waypoints are stored in order of insertion, starting with the top row
    (
        result,
        waypoint_name_to_coordinates,
    ) = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
        WAYPOINT_FILE_PATH,
    )

    if not result:
        print("ERROR: load_waypoint_name_to_coordinates_map")
        return -1

    result, waypoints_list = waypoints_dict_to_list.waypoints_dict_to_list(
        waypoint_name_to_coordinates,
    )
    if not result:
        print("ERROR: convert waypoints from dict to list")
        return -1
    print("Content of waypoints_list:", waypoints_list)

    result, waypoint_commands = waypoints_to_commands.waypoints_to_commands(
        waypoints_list, ALTITUDE
    )
    if not result:
        print("Error: waypoints_to_commands")
        return -1

    (
        result,
        takeoff_landing_commands,
    ) = add_takeoff_and_landing_command.add_takeoff_and_landing_command(waypoint_commands, ALTITUDE)
    if not result:
        print("Error: add_takeoff_and_landing_command")
        return -1

    result = upload_commands.upload_commands(drone, takeoff_landing_commands, DRONE_TIMEOUT)
    if not result:
        print("Error: upload_commands")
        return -1

    is_qr_text_found = False
    # Drone starts flying
    while True:
        result, waypoint_info = waypoint_tracking.get_current_waypoint_info(drone)
        if not result:
            print("Error: waypoint_tracking (waypoint_info)")
        else:
            print(f"Current waypoint sequence: {waypoint_info}")

        result, location = waypoint_tracking.get_current_location(drone)
        if not result:
            print("Error: waypoint_tracking (get_current_location)")
        else:
            print(f"Current location (Lat, Lon): {location}")

        is_qr_text_found = False
        # nonblocking, just takes single picture
        # is_qr_text_found, diversion_qr_text = diversion_qr_input.diversion_qr_input(CAMERA)
        # wait for text input in console
        print("Press 'q' to simulate QR code found.")
        if not is_qr_text_found:
            # Check if input is available
            if msvcrt.kbhit():
                input_char = msvcrt.getwche()
                if input_char == "q":
                    is_qr_text_found = True
                    print("Simulated QR code found.")

        # run once when qr code is detected
        if is_qr_text_found:

            # Read in hardcoded waypoints from CSV file
            # Waypoints are stored in order of insertion, starting with the top row
            (result, diversion_waypoint_list) = (
                load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
                    DIVERSION_WAYPOINT_FILE_PATH,
                )
            )
            if not result:
                print("ERROR: diversion_waypoint_name_to_coordinates_map")
                return -1

            diversion_waypoint_values_list = list(diversion_waypoint_list.values())

            (result, rejoin_waypoint_list) = (
                load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
                    REJOIN_WAYPOINT_FILE_PATH,
                )
            )
            if not result:
                print("ERROR: rejoin_waypoint_name_to_coordinates_map")
                return -1

            # convert tuple[float, float] to location ground
            current_latitude, current_longitude = location
            result, named_location = location_global.LocationGlobal.create(
                current_latitude, current_longitude
            )
            if not result:
                print("ERROR: Could not create named location")
                return -1

            waypoints_around_diversion = (
                diversion_waypoints_from_vertices.diversion_waypoints_from_vertices(
                    named_location,
                    next(iter(rejoin_waypoint_list.values())),
                    diversion_waypoint_values_list,
                )
            )

            result, waypoints_around_diversion_commands = (
                waypoints_to_commands.waypoints_to_commands(waypoints_around_diversion, ALTITUDE)
            )
            if not result:
                print("Error: diversion_waypoints_to_commands")
                return -1

            # add the waypoint_around_diversion in between current commands
            # rest of commands starting from rejoin waypoint
            first_key = next(iter(rejoin_waypoint_list))
            waypoints_after_diversion = waypoints_list[
                waypoints_list.index(rejoin_waypoint_list[first_key]) :
            ]

            result, waypoints_after_diversion_commands = (
                waypoints_to_commands.waypoints_to_commands(waypoints_after_diversion, ALTITUDE)
            )
            if not result:
                print("Error: post_diversion_waypoints_to_commands")
                return -1

            # combine diversion commands and regular commands after diversion
            diversion_route_commands = (
                waypoints_around_diversion_commands + waypoints_after_diversion_commands
            )

            # add landing command at the end
            landing_command = generate_command.landing()
            diversion_route_commands.append(landing_command)

            print("Commands ready to upload")
            # upload waypoint_around_diversion + waypoints_after_diversion as new ones
            result = upload_commands.upload_commands(drone, diversion_route_commands, DRONE_TIMEOUT)
            if not result:
                print("Error: diversion_route_upload_commands")
                return -1

        time.sleep(DELAY)

    return 0


# pylint: enable=duplicate-code


if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
