"""
Task 1 path.
"""

import dronekit


CONNECTION_ADDRESS = "tcp:localhost:14550"


def run() -> int:
    """
    Uploads mission to run a maximum number of laps and monitors the mission for early landing.
    """
    # Wait ready is false as the drone may be on the ground
    drone = dronekit.connect(CONNECTION_ADDRESS, wait_ready = False)

    return 0


if __name__ == "__main__":
    # Not a constant
    # pylint: disable-next=invalid-name
    result_run = run()
    if result_run < 0:
        print("ERROR")

    print("Done")