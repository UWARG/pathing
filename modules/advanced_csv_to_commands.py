"""
An command generator with advanced parameters and greater flexibility
"""

import pathlib

import dronekit


VALID_FRAMES = {
    "global": dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL,
    "global_relative_alt": dronekit.mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
}

VALID_COMMANDS = {
    "land": dronekit.mavutil.mavlink.MAV_CMD_NAV_LAND,
    "return_to_launch": dronekit.mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
    "takeoff": dronekit.mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    "waypoint": dronekit.mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
    "waypoint_spline": dronekit.mavutil.mavlink.MAV_CMD_NAV_SPLINE_WAYPOINT,
    "loiter_timed": dronekit.mavutil.mavlink.MAV_CMD_NAV_LOITER_TIME,
    "loiter_unlimited": dronekit.mavutil.mavlink.MAV_CMD_NAV_LOITER_UNLIM,
    "do_jump": dronekit.mavutil.mavlink.MAV_CMD_DO_JUMP,
}


def generate_command_advanced(
    frame: str,
    command_type: str,
    param1: float,  # I'm anxious about this because of do_jump which requires ints
    param2: float,
    param3: float,
    param4: float,
    param5: float,
    param6: float,
    param7: float,
) -> "tuple[bool,dronekit.Command]":
    """
    Parameters:

    frame: The command's frame of reference. Frame should be one of the following two values.
        - global (usually used for landing or return to launch)
        - global_relative_alt (all other commands, such as waypoint, spline waypoint, etc.)

    command_type: The command type. Depending on this value, params 1 through 7 will take on different meanings. This should be one of the following enums:
        - land:
        - return_to_launch: Return to the home location where the vehicle was last armed.
        - takeoff
        - waypoint: Navigate to the specified waypoint
        - waypoint_spline
        - loiter_timed: Loiter at the specified location for an specified amount of time
        - loiter_unlimited: Loiter at the specified location for an unlimited amount of time
        - do_jump: Jump to the specified command in the mission list.

    param1 through param7: These take different meanings depending on the command type. See the documentation for meanings:
                            https://uwarg-docs.atlassian.net/wiki/spaces/CV/pages/2567274629/Encoded+MAVLink+commands
                            Alteratively, here is the official documentation:
                            https://ardupilot.org/copter/docs/common-mavlink-mission-command-messages-mav_cmd.html#commands-supported-by-copter

    Returns: Whether or not the command was successful, and the mission command.
    """

    # Invalid command
    if command_type not in VALID_COMMANDS:
        return False, None

    # Invalid frame type
    if frame not in VALID_FRAMES:
        return False, None

    return True, dronekit.Command(
        0,
        0,
        0,
        VALID_FRAMES[frame],
        VALID_COMMANDS[command_type],
        0,
        0,
        param1,
        param2,
        param3,
        param4,
        param5,
        param6,
        param7,
    )


def csv_to_commands_list(
    mission_file_path: pathlib.Path,
) -> "tuple[bool, list[dronekit.Command]]":
    """
    A method that reads a list of advanced commands from a csv file and generates a mission.
    Parameters:
        - mission_file_path: The advanced csv file containing the different mission commands

    Returns:
        - Whether or not the mission was successfully created
        - A list of dronekit commands that represent the mission

    """
    # Does the file path exist?
    if not mission_file_path.exists():
        return False, None

    mission = []
    with open(mission_file_path, encoding="utf-8") as file:
        for line in file:
            # Skip header and empty lines
            parts = line.split(",")
            if line in "frame,command_type,param1,param2,param3,param4,param5,param6,param7\n":
                continue

            # If the parameters are messed up
            if len(parts) != 9:
                return False, None

            frame, command_type, param1, param2, param3, param4, param5, param6, param7 = parts
            success, command = generate_command_advanced(
                frame,
                command_type,
                float(param1),
                float(param2),
                float(param3),
                float(param4),
                float(param5),
                float(param6),
                float(param7),
            )
            # Was the command successfully generated?
            if not success:
                return False, None

            mission.append(command)

    if len(mission) > 0:
        return True, mission

    return False, None
