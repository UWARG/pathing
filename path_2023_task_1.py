"""
Reads waypoints from QR code and sends drone commands.
"""

import pathlib
import time
import sys
import select
import msvcrt

import dronekit

from modules import add_takeoff_and_landing_command
from modules import load_waypoint_name_to_coordinates_map
from modules import qr_input
from modules import diversion_qr_input
from modules import qr_to_waypoint_names
from modules import upload_commands
from modules import waypoint_names_to_coordinates
from modules import waypoint_tracking
from modules import waypoints_dict_to_list
from modules import waypoints_to_commands
from modules import diversion_waypoints_from_vertices
from modules import diversion_qr_to_waypoint_list
from modules import generate_command

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

    # result, qr_text = qr_input.qr_input(CAMERA)
    # if not result:
    #     print("ERROR: qr_input")
    #     return -1

    # result, waypoint_names = qr_to_waypoint_names.qr_to_waypoint_names(qr_text)
    # if not result:
    #     print("ERROR: qr_to_waypoint_names")
    #     return -1

    # result, waypoints = waypoint_names_to_coordinates.waypoint_names_to_coordinates(
    #     waypoint_names,
    #     waypoint_name_to_coordinates,
    # )
    # if not result:
    #     print("ERROR: waypoint_names_to_coordinates")
    #     return -1

    result, waypoint_commands = waypoints_to_commands.waypoints_to_commands(waypoints_list, ALTITUDE)
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
        print("Press 'q' to simulate QR code found or any other key to continue waiting.")
        if not is_qr_text_found:
            # Check if input is available
            if msvcrt.kbhit():
                input_char = msvcrt.getwche() 
                if input_char == 'q':
                    is_qr_text_found = True
                    print("Simulated QR code found.")

        # this part should run only once when new qrcode is passed through
        if is_qr_text_found:

            # result, diversion_waypoint_information = diversion_qr_to_waypoint_list.diversion_qr_to_waypoint_list(DIVERSION_WAYPOINT_FILE_PATH)
            # if not result:
            #     print("ERROR: diversion_qr_to_waypoint_list")
            #     return -1
            
            # Read in hardcoded waypoints from CSV file
            # Waypoints are stored in order of insertion, starting with the top row
            (result, diversion_waypoint_list) = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
                DIVERSION_WAYPOINT_FILE_PATH,
            )
            if not result:
                print("ERROR: diversion_waypoint_name_to_coordinates_map")
                return -1
            
            diversion_waypoint_values_list = list(diversion_waypoint_list.values())

            (result, rejoin_waypoint_list) = load_waypoint_name_to_coordinates_map.load_waypoint_name_to_coordinates_map(
                REJOIN_WAYPOINT_FILE_PATH,
            )
            if not result:
                print("ERROR: rejoin_waypoint_name_to_coordinates_map")
                return -1

            print("rejoin_waypoint_list:", rejoin_waypoint_list)

            print("diversion_waypoint_list:", diversion_waypoint_values_list)
            print("length: ", len(diversion_waypoint_values_list))

            waypoints_around_diversion = diversion_waypoints_from_vertices.diversion_waypoints_from_vertices(
                location,
                next(iter(rejoin_waypoint_list.values())),
                diversion_waypoint_values_list,
            )
            print("made waypoints_around_diversion")

            result, waypoints_around_diversion_commands = waypoints_to_commands.waypoints_to_commands(waypoints_around_diversion, ALTITUDE)
            if not result:
                print("Error: diversion_waypoints_to_commands")
                return -1
            
            # add the waypoint_around_diversion in between current commands
            # rest of commands starting from rejoin waypoint
            waypoints_after_diversion_commands = waypoint_commands[waypoint_commands.index(rejoin_waypoint_list[0]):]

            result, waypoints_after_diversion_commands = waypoints_to_commands.waypoints_to_commands(waypoints_after_diversion_commands, ALTITUDE)
            if not result:
                print("Error: post_diversion_waypoints_to_commands")
                return -1
            
            # combine diversion commands and regular commands after diversion
            diversion_route_commands = waypoints_around_diversion_commands + waypoints_after_diversion_commands
            
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
