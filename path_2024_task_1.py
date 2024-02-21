'''
Task 1 path
'''

import dronekit


CONNECTION_ADDRESS = "tcp:localhost:14550"


def run() -> int:
    """
    Reads in hardcoded waypoints from CSV file and sends drone commands.
    """
    # Wait ready is false as the drone may be on the ground
    drone = dronekit.connect(CONNECTION_ADDRESS, wait_ready = False)