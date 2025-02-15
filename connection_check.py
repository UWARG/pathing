"""
For testing MAVLink connection with FlightController.
"""

import time

from modules.common.modules.mavlink import flight_controller


# Set these to test what you want to test
WRITE_TEST = False  # Sends a hardcoded test mission to the drone
READ_TEST = True  # Receives and prints drone telemetry

# Change this to the actual connection
CONNECTION_ADDRESS = "tcp:localhost:14550"

ALTITUDE = 40  # metres


def write_test_mission(drone: flight_controller.FlightController) -> bool:
    """
    Creates and sends a hardcoded test mission to the drone.
    """

    result = drone.drone.commands.clear()

    if not result:
        print("ERROR: Could not clear mission.")
        return False

    # Create and upload commands
    result = drone.insert_waypoint(0, -35.3632610, 149.1691446, ALTITUDE)

    if not result:
        print("ERROR: Could not upload command 0.")
        return False

    result = drone.insert_waypoint(1, -35.3603736, 149.1689944, ALTITUDE)

    if not result:
        print("ERROR: Could not upload command 1.")
        return False

    return True


def read_data(drone: flight_controller.FlightController) -> bool:
    """
    Prints drone telemetry and mission status.
    """
    result, odometry = drone.get_odometry()

    if not result:
        print("ERROR: Could not get odometry.")
        return False

    print("------")
    print("Position:")
    print(odometry.position.altitude)
    print(odometry.position.latitude)
    print(odometry.position.longitude)
    print("Attitude:")
    print(odometry.orientation.pitch)
    print(odometry.orientation.roll)
    print(odometry.orientation.yaw)

    result, commands = drone.download_commands()

    if not result:
        print("ERROR: Could not get commands.")
        return False

    result, next_waypoint = drone.get_next_waypoint()

    if not result:
        print("ERROR: Could not get next waypoint.")
        return False

    print("Command information:")
    print("Waypoint total count: " + str(commands.count()))
    print("Next waypoint index: " + str(next_waypoint.index()))

    return True


def main() -> int:
    """
    Main function.
    """
    result, flight_controller_vehicle = flight_controller.FlightController.create(
        CONNECTION_ADDRESS
    )

    if not result:
        print("ERROR: Could not connect to the flight controller.")
        return -1

    if WRITE_TEST:
        write_test_mission(flight_controller_vehicle)

    if READ_TEST:
        for _ in range(0, 40):
            read_data(flight_controller_vehicle)
            time.sleep(0.5)

    flight_controller_vehicle.close()

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
