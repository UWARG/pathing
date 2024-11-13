"""
Command generators.
"""

from pymavlink import mavutil

from .common.modules.mavlink import dronekit


LANDING_FRAME = mavutil.mavlink.MAV_FRAME_GLOBAL
RTL_FRAME = mavutil.mavlink.MAV_FRAME_GLOBAL
TAKEOFF_FRAME = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
WAYPOINT_FRAME = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
WAYPOINT_SPLINE_FRAME = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
LOITER_TIMED_FRAME = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
LOITER_UNLIMITED_FRAME = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT
DO_JUMP_FRAME = mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT


def landing() -> dronekit.Command:
    """
    Returns landing command.
    """
    return dronekit.Command(
        0,
        0,
        0,
        LANDING_FRAME,
        mavutil.mavlink.MAV_CMD_NAV_LAND,
        0,
        0,
        0,  # param1
        0,
        0,
        0,
        0,
        0,
        0,
    )


def return_to_launch() -> dronekit.Command:
    """
    Returns RTL command.
    """
    return dronekit.Command(
        0,
        0,
        0,
        RTL_FRAME,
        mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
        0,
        0,
        0,  # param1
        0,
        0,
        0,
        0,
        0,
        0,
    )


def takeoff(altitude: float) -> dronekit.Command:
    """
    Returns takeoff command.

    altitude: Metres.
    """
    return dronekit.Command(
        0,
        0,
        0,
        TAKEOFF_FRAME,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0,
        0,
        0,  # param1
        0,
        0,
        0,
        0,
        0,
        altitude,
    )


def waypoint(
    hold_time: float, acceptance_radius: float, latitude: float, longitude: float, altitude: float
) -> dronekit.Command:
    """
    Returns waypoint command.

    hold_time: Seconds.
    acceptance_radius: Metres.
    latitude: Decimal degrees.
    longitude: Decimal degrees.
    altitude: Metres.
    """
    return dronekit.Command(
        0,
        0,
        0,
        WAYPOINT_FRAME,
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
        0,
        0,
        hold_time,  # param1
        acceptance_radius,
        0,
        0,
        latitude,
        longitude,
        altitude,
    )


def waypoint_spline(
    hold_time: float, latitude: float, longitude: float, altitude: float
) -> dronekit.Command:
    """
    Returns waypoint spline command.

    hold_time: Seconds.
    latitude: Decimal degrees.
    longitude: Decimal degrees.
    altitude: Metres.
    """
    return dronekit.Command(
        0,
        0,
        0,
        WAYPOINT_SPLINE_FRAME,
        mavutil.mavlink.MAV_CMD_NAV_SPLINE_WAYPOINT,
        0,
        0,
        hold_time,  # param1
        0,
        0,
        0,
        latitude,
        longitude,
        altitude,
    )


def loiter_timed(
    loiter_time: float, latitude: float, longitude: float, altitude: float
) -> dronekit.Command:
    """
    Returns loiter timed command.

    loiter_time: Seconds.
    latitude: Decimal degrees.
    longitude: Decimal degrees.
    altitude: Metres.
    """
    return dronekit.Command(
        0,
        0,
        0,
        LOITER_TIMED_FRAME,
        mavutil.mavlink.MAV_CMD_NAV_LOITER_TIME,
        0,
        0,
        loiter_time,  # param1
        0,
        0,
        0,
        latitude,
        longitude,
        altitude,
    )


def loiter_unlimited(latitude: float, longitude: float, altitude: float) -> dronekit.Command:
    """
    Returns loiter unlimited command.

    latitude: Decimal degrees.
    longitude: Decimal degrees.
    altitude: Metres.
    """
    return dronekit.Command(
        0,
        0,
        0,
        LOITER_UNLIMITED_FRAME,
        mavutil.mavlink.MAV_CMD_NAV_LOITER_UNLIM,
        0,
        0,
        0,  # param1
        0,
        0,
        0,
        latitude,
        longitude,
        altitude,
    )


def do_jump(waypoint_sequence_number: int, repeat: int) -> dronekit.Command:
    """
    Returns do jump command.

    waypoint_sequence_number: The sequence number of the mission command to jump to.
    repeat: Maximum number of times to perform the jump.
    """
    return dronekit.Command(
        0,
        0,
        0,
        DO_JUMP_FRAME,
        mavutil.mavlink.MAV_CMD_DO_JUMP,
        0,
        0,
        waypoint_sequence_number,  # param1
        repeat,
        0,
        0,
        0,
        0,
        0,
    )
