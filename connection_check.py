"""
For testing MAVLink connection with FlightController.
"""

import time

from pymavlink import mavutil

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
    commands = []

    # Create and add commands
    command0 = flight_controller.dronekit.Command(
        0,
        0,
        0,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
        0,
        0,
        0,  # param1
        10,
        0,
        0,
        -35.3632610,
        149.1691446,
        ALTITUDE,
    )

    commands.append(command0)

    command1 = flight_controller.dronekit.Command(
        0,
        0,
        0,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
        0,
        0,
        0,  # param1
        10,
        10,
        0,
        -35.3603736,
        149.1689944,
        ALTITUDE,
    )

    commands.append(command1)

    # Get the set of commands from the drone
    result, command_sequence = drone.download_commands()

    if not result:
        print("ERROR: Could not download commands.")
        return False

    command_sequence.clear()

    for command in commands:
        command_sequence.add(command)

    # Upload commands to drone
    result = drone.upload_commands(command_sequence)

    if not result:
        print("ERROR: Could not upload commands.")
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

    print("Command information:")
    print("Waypoint total count: " + str(drone.drone.commands.count))
    print("Next waypoint index: " + str(drone.drone.commands.next))

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
