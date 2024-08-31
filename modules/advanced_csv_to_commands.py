"""
An command generator with advanced parameters and greater flexibility
"""

import pathlib

from pymavlink import mavutil

from .common.mavlink import dronekit


VALID_FRAMES = {
    "global": mavutil.mavlink.MAV_FRAME_GLOBAL,
    "global_relative_alt": mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
}

VALID_COMMANDS = {
    "land": mavutil.mavlink.MAV_CMD_NAV_LAND,
    "return_to_launch": mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH,
    "takeoff": mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    "waypoint": mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
    "waypoint_spline": mavutil.mavlink.MAV_CMD_NAV_SPLINE_WAYPOINT,
    "loiter_timed": mavutil.mavlink.MAV_CMD_NAV_LOITER_TIME,
    "loiter_unlimited": mavutil.mavlink.MAV_CMD_NAV_LOITER_UNLIM,
    "do_jump": mavutil.mavlink.MAV_CMD_DO_JUMP,
}

"""
The input matrix maps the command types to the valid parameters.
See documentation for more information: https://uwarg-docs.atlassian.net/wiki/spaces/CV/pages/2567274629/Encoded+MAVLink+commands 
0: Parameter should be set to zero
1: Parameter should be a float
2: Parameter should be an integer
"""
COMMAND_TO_PARAMETER_MATRIX = {
    "land": [0, 0, 0, 0, 1, 1, 0],
    "return_to_launch": [0, 0, 0, 0, 0, 0, 0],
    "takeoff": [0, 0, 0, 0, 0, 0, 1],
    "waypoint": [1, 1, 0, 0, 1, 1, 1],
    "waypoint_spline": [1, 0, 0, 0, 1, 1, 1],
    "loiter_timed": [1, 0, 0, 0, 1, 1, 1],
    "loiter_unlimited": [0, 0, 0, 0, 1, 1, 1],
    "do_jump": [2, 2, 0, 0, 0, 0, 0],
}


def check_validity(params: "list[float]", matrix_rules: "list[float]") -> bool:
    """
    Compares a command's parameters to the matrix rules, and returns whether
    the command is valid or not
    """
    if len(params) != len(matrix_rules):
        return False

    for index, param in enumerate(params):
        if matrix_rules[index] == 0 and param != 0:
            return False
        if matrix_rules[index] == 2 and not param.is_integer():
            return False

    return True


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
) -> "tuple[bool,dronekit.Command | None]":
    """
    Parameters: See documentation: https://uwarg-docs.atlassian.net/wiki/spaces/CV/pages/2567274629/Encoded+MAVLink+commands

    Returns: Whether the command was successful and the mission command.
    """

    # Invalid command
    if command_type not in VALID_COMMANDS:
        return False, None

    # Invalid frame type
    if frame not in VALID_FRAMES:
        return False, None

    params = [param1, param2, param3, param4, param5, param6, param7]

    if not check_validity(params, COMMAND_TO_PARAMETER_MATRIX[command_type]):
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
) -> "tuple[bool, list[dronekit.Command] | None]":
    """
    A method that reads a list of advanced commands from a csv file and generates a mission.
    Parameters:
        - mission_file_path: The advanced csv file containing the different mission commands

    Returns:
        - Whether or not the mission was successfully created
        - A list of dronekit commands that represent the mission

    """
    if not mission_file_path.exists():
        return False, None

    mission = []
    with open(mission_file_path, encoding="utf-8") as file:
        for line in file:
            # Skip header and empty lines
            if line in "frame,command_type,param1,param2,param3,param4,param5,param6,param7\n":
                continue

            parts = line.split(",")

            # Incorrect number of parameters
            if len(parts) != 9:
                return False, None

            frame, command_type, param1, param2, param3, param4, param5, param6, param7 = parts
            result, command = generate_command_advanced(
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
            if not result:
                return False, None

            mission.append(command)

    if len(mission) == 0:
        return False, None

    return True, mission
