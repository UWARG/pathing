"""
Test process
"""

import dronekit

from modules import add_takeoff_and_landing_command


def test_add_takeoff_and_landing_command():
    """
    Tests functionality correctness of add_takeoff_and_landing_command
    """
    commands = []
    altitude = 50

    commands_actual = add_takeoff_and_landing_command.add_takeoff_and_landing_command(commands, altitude)

    assert isinstance(commands_actual, list)
    assert len(commands_actual) == 2

    # Test takeoff command
    takeoff_command = commands_actual[0]
    assert isinstance(takeoff_command, dronekit.Command)
    assert takeoff_command.frame == add_takeoff_and_landing_command.MAVLINK_TAKEOFF_FRAME
    assert takeoff_command.command == add_takeoff_and_landing_command.MAVLINK_TAKEOFF_COMMAND
    assert takeoff_command.param7 == altitude

    # Test landing command
    landing_command = commands_actual[1]
    assert isinstance(landing_command, dronekit.Command)
    assert landing_command.frame == add_takeoff_and_landing_command.MAVLINK_LANDING_FRAME
    assert landing_command.command == add_takeoff_and_landing_command.MAVLINK_LANDING_COMMAND

    # Ensure the commands list is unmodified
    assert len(commands) == 0
