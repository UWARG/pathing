"""
For testing MAVLink connection with Common-repository FlightController.
"""

import pathlib
import time
import yaml

from modules.common.mavlink.modules.flight_controller import FlightController

# Set these to test what you want to test
WRITE_TEST = False  # Sends a hardcoded test mission to the drone
READ_TEST = True  # Receives and prints drone telemetry

CONFIG_FILE_PATH = pathlib.Path("config.yaml")

def main():
    """
    Main function.
    """

    # Open config file
    try:
        with CONFIG_FILE_PATH.open("r", encoding="utf8") as file:
            try:
                config = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(f"Error parsing YAML file: {exc}")
    except FileNotFoundError:
        print(f"File not found: {CONFIG_FILE_PATH}")
        return -1
    except IOError as exc:
        print(f"Error when opening file: {exc}")
        return -1
    
    try:
        TAKEOFF_ALTITUDE = config["takeoff_altitude"]
        CONNECTION_ADDRESS = config["connection_address"]
    except KeyError:
        print("Config key(s) not found")
        return -1

    success, controller = FlightController.create(CONNECTION_ADDRESS)
    
    if success < 0:
        print("ERROR: FlightController failed to instantiate")
        return -1
    
    controller.get_odometry()
    
    return 0

if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
