"""
For testing MAVLink connection with DroneKit-Python.
"""

import time

from pymavlink import mavutil

from modules.common.mavlink import dronekit


# Set these to test what you want to test
WRITE_TEST = False  # Sends a hardcoded test mission to the drone
READ_TEST = True  # Receives and prints drone telemetry

# Change this to the actual connection
CONNECTION_ADDRESS = "tcp:localhost:14550"

ALTITUDE = 40  # metres


def write_test_mission(drone: dronekit.Vehicle) -> bool:
    """
    Creates and sends a hardcoded test mission to the drone.
    """
    commands = []

    # Create and add commands
    command0 = dronekit.Command(
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

    command1 = dronekit.Command(
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
    command_sequence = drone.commands
    command_sequence.download()
    command_sequence.wait_ready()
    command_sequence.clear()
    for command in commands:
        command_sequence.add(command)

    # Upload commands to drone
    command_sequence.upload()

    return True


def read_data(drone: dronekit.Vehicle) -> bool:
    """
    Prints drone telemetry and mission status.
    """
    print("------")
    print("Position:")
    print(drone.location.global_frame.alt)
    print(drone.location.global_frame.lat)
    print(drone.location.global_frame.lon)
    print("Attitude:")
    print(drone.attitude.pitch)
    print(drone.attitude.roll)
    print(drone.attitude.yaw)

    command_sequence = drone.commands

    command_sequence.download()
    command_sequence.wait_ready()

    print("Command information:")
    print("Waypoint total count: " + str(command_sequence.count))
    print("Next waypoint index: " + str(command_sequence.next))


def main() -> int:
    """
    Main function.
    """
    # TODO: Fails when wait_ready=True, debugging why this is
    # wait_ready=False is dangerous
    dronekit_vehicle = dronekit.connect(CONNECTION_ADDRESS, wait_ready=False)

    if WRITE_TEST:
        write_test_mission(dronekit_vehicle)

    if READ_TEST:
        for _ in range(0, 40):
            read_data(dronekit_vehicle)
            time.sleep(0.5)

    dronekit_vehicle.close()

    return 0


if __name__ == "__main__":
    result_main = main()
    if result_main < 0:
        print(f"ERROR: Status code: {result_main}")

    print("Done!")
