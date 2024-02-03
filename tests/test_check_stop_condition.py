"""
Test the drone stop condition
"""

import dronekit
import pytest
import time

from modules import check_stop_condition


MAVLINK_LANDING_FRAME = dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL
MAVLINK_LANDING_COMMAND = dronekit.mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH
MAXIMUM_FLIGHT_TIME = 5  # seconds
START_TIME = 0

@pytest.fixture
def start_time() -> float:
    """
    Fixture to get current time
    """
    yield time.time()

def test_current_time_within_max_time(start_time: float, drone: dronekit.Vehicle):
    """
    Test stop condition with current time within max time.
    """
    valid_current_time = start_time + MAXIMUM_FLIGHT_TIME*0.5
    result = check_stop_condition.check_stop_condition(start_time, valid_current_time, drone, MAXIMUM_FLIGHT_TIME)

    assert not result  # Expect False



def test_current_time_exceeds_max_time(start_time: float, drone: dronekit.Vehicle):
    """
    Test stop condition with current time exceeding max time.
    """
    invalid_current_time = start_time + MAXIMUM_FLIGHT_TIME*1.5
    result = check_stop_condition.check_stop_condition(start_time, invalid_current_time, drone, MAXIMUM_FLIGHT_TIME)

    assert result  # expect True
