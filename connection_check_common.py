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
    
    if WRITE_TEST:
        assert(NotImplementedError)
        return -1

    if READ_TEST:
        success, odometry = controller.get_odometry()
        print("------")
        print("Position:")
        print(odometry.position.altitude)
        print(odometry.position.latitude)
        print(odometry.position.longitude)
        print("Attitude:")
        print(odometry.orientation.pitch)
        print(odometry.orientation.roll)
        print(odometry.orientation.yaw)
        # i dont think theres code to download from flight controller yet 💀
    
    return 0

if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
