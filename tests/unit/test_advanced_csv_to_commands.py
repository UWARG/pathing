"""
Testing the advanced_csv_to_commands module
"""

import pathlib

from modules import advanced_csv_to_commands
from modules import generate_command
from modules.common.modules.mavlink import flight_controller


def test_normal_file() -> None:
    """
    A normal advanced CSV file
    """
    normal_advanced_csv_path = pathlib.Path(
        "tests", "test_csv", "advanced_csv", "test_normal_advanced_csv.csv"
    )

    expected_mission = [
        generate_command.takeoff(50),
        generate_command.loiter_timed(6.0, 43.47323264522664, -80.5401164, 50),
        generate_command.loiter_unlimited(43.47, -80.55, 50),
        generate_command.waypoint(0, 0.1, 43.47352476, -80.54144668, 10),
        generate_command.waypoint_spline(0, 43.47323264522664, -80.5401164, 10),
        generate_command.return_to_launch(),
        generate_command.landing(),
        generate_command.do_jump(4, 2),
    ]

    success, mission = advanced_csv_to_commands.csv_to_commands_list(normal_advanced_csv_path)

    # Test
    assert success
    assert isinstance(mission, list)
    assert len(mission) == len(expected_mission)

    for idx, command in enumerate(mission):
        assert isinstance(command, flight_controller.dronekit.Command)
        assert command.frame == expected_mission[idx].frame
        assert command.command == expected_mission[idx].command
        assert command.param1 == expected_mission[idx].param1
        assert command.param2 == expected_mission[idx].param2
        assert command.param3 == expected_mission[idx].param3
        assert command.param4 == expected_mission[idx].param4
        assert command.x == expected_mission[idx].x
        assert command.y == expected_mission[idx].y
        assert command.z == expected_mission[idx].z


def test_empty_csv() -> None:
    """
    CSV file is empty, expected to fail
    """
    empty_advanced_csv_path = pathlib.Path(
        "tests", "test_csv", "advanced_csv", "test_empty_advanced_csv.csv"
    )
    success, mission = advanced_csv_to_commands.csv_to_commands_list(empty_advanced_csv_path)
    assert not success
    assert mission is None


def test_invalid_command_name() -> None:
    """
    waypoint is misspelled as "wayypoint", expected to fail
    """
    invalid_command_name_path = pathlib.Path(
        "tests", "test_csv", "advanced_csv", "test_invalid_command_name.csv"
    )
    success, mission = advanced_csv_to_commands.csv_to_commands_list(invalid_command_name_path)
    assert not success
    assert mission is None


def test_invalid_frame_name() -> None:
    """
    global is misspelled as "globbal", expected to fail
    """
    invalid_frame_name_path = pathlib.Path(
        "tests", "test_csv", "advanced_csv", "test_invalid_frame_name.csv"
    )
    success, mission = advanced_csv_to_commands.csv_to_commands_list(invalid_frame_name_path)
    assert not success
    assert mission is None


def test_file_path_does_not_exist() -> None:
    """
    The file path does not exist, expected to fail
    """
    invalid_path = pathlib.Path("tests", "test_csv", "path_DNE.csv")
    success, mission = advanced_csv_to_commands.csv_to_commands_list(invalid_path)
    assert not success
    assert mission is None


def test_bad_line() -> None:
    """
    A line does not have the correct number of parameters.
    Fourth line (third command) is missing a 0 and therefore an invalid command
    """
    invalid_path = pathlib.Path(
        "tests", "test_csv", "advanced_csv", "test_incorrect_num_params_csv.csv"
    )
    success, mission = advanced_csv_to_commands.csv_to_commands_list(invalid_path)
    assert not success
    assert mission is None


def test_nonzero_param() -> None:
    """
    A parameter that should be set to zero is not zero (takeoff param1),
    expected to fail
    """
    nonzero_param_path = pathlib.Path(
        "tests", "test_csv", "advanced_csv", "test_nonzero_param_csv.csv"
    )
    success, mission = advanced_csv_to_commands.csv_to_commands_list(nonzero_param_path)
    assert not success
    assert mission is None


def test_non_int_param() -> None:
    """
    Do-jump's parameters are supposed to be integers but they are not,
    expected to fail
    """
    non_integer_param_path = pathlib.Path(
        "tests", "test_csv", "advanced_csv", "test_non_integer_param_csv.csv"
    )
    success, mission = advanced_csv_to_commands.csv_to_commands_list(non_integer_param_path)
    assert not success
    assert mission is None
