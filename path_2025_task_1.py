"""
Should write located IR beacons to a kml file for task 1
File is a work in progress and should not be run yet
"""

import pathlib
import time
import yaml

from modules import check_stop_condition
from modules.common.modules.mavlink import dronekit

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
        # pylint: disable=unused-variable
        DRONE_TIMEOUT = config["drone_timeout"]
        TAKEOFF_ALTITUDE = config["takeoff_altitude"]
        # pylint: enable=unused-variable
        # pylint: enable=invalid-name
    except KeyError as exc:
        print(f"Unable to find key in yaml file: {exc}")
        return -1

    pathlib.Path(LOG_DIRECTORY_PATH).mkdir(exist_ok=True)

    # Wait ready is false as the drone may be on the ground
    drone = dronekit.connect(CONNECTION_ADDRESS, wait_ready=False)

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
