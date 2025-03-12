"""
Test plotting waypoints in a circular fashion around a center
"""

import pathlib

import pytest

from modules import plot_circular_path
from modules.common.modules import position_global_relative_altitude


DEFAULT_TOLERANCE = 1e-6


def verify_close_enough(
    actual: position_global_relative_altitude.PositionGlobalRelativeAltitude,
    expected: position_global_relative_altitude.PositionGlobalRelativeAltitude,
    tolerance: float,
) -> bool:
    """
    Check equality of positions.
    """
    if not actual.latitude == pytest.approx(expected.latitude, rel=tolerance):
        return False

    if not actual.longitude == pytest.approx(expected.longitude, rel=tolerance):
        return False

    if not actual.relative_altitude == pytest.approx(expected.relative_altitude, rel=tolerance):
        return False

    return True


class TestMoveOffset:
    """
    Test move_coordinates_by_offset function.
    """

    def test_normal(self) -> None:
        """
        Move the drone north east.
        """
        # Setup
        result, starting_point = (
            position_global_relative_altitude.PositionGlobalRelativeAltitude.create(10, 12, 1)
        )
        assert result
        assert starting_point is not None

        offset_x = 100_000  # east
        offset_y = 100_000  # north

        result, expected = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
            10.902630923020318, 12.914531732240036, 1
        )
        assert result
        assert expected is not None

        # Run
        result, actual = plot_circular_path.move_coordinates_by_offset(
            starting_point, offset_x, offset_y
        )

        # Check
        assert result
        assert actual is not None

        assert verify_close_enough(actual, expected, DEFAULT_TOLERANCE)


class TestGenerateCircularPath:
    """
    Test generate_circular_path function.
    """

    def test_normal(self) -> None:
        """
        Generate a circular path.
        """
        # Setup
        result, centre = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
            0, 0, 1
        )
        assert result
        assert centre is not None

        radius = 111_319
        num_points = 20
        expected_points = [
            (0, 1),
            (0.309016994, 0.951056516),
            (0.587785252, 0.809016994),
            (0.809016994, 0.587785252),
            (0.951056516, 0.309016994),
            (1, 6.12574e-17),
            (0.951056516, -0.309016994),
            (0.809016994, -0.587785252),
            (0.587785252, -0.809016994),
            (0.309016994, -0.951056516),
            (1.22515e-16, -1),
            (-0.309016994, -0.951056516),
            (-0.587785252, -0.809016994),
            (-0.809016994, -0.587785252),
            (-0.951056516, -0.309016994),
            (-1, -1.83772e-16),
            (-0.951056516, 0.309016994),
            (-0.809016994, 0.587785252),
            (-0.587785252, 0.809016994),
            (-0.309016994, 0.951056516),
            (0, 1),
        ]
        assert len(expected_points) == num_points + 1

        # Run
        result, waypoints = plot_circular_path.generate_circular_path(centre, radius, num_points)

        # Check
        assert result
        assert waypoints is not None

        # Reduced tolerance as the planet is a not a sphere
        tolerance = 1e-2

        assert len(waypoints) == num_points + 1
        for i in range(num_points):
            actual = waypoints[i]
            assert actual is not None

            expected_latitude, expected_longitude = expected_points[i]
            result, expected = (
                position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
                    expected_latitude, expected_longitude, centre.relative_altitude
                )
            )

            assert verify_close_enough(actual, expected, tolerance)

    invalid_inputs = [
        (
            position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
                3.99, 12.6, 3.4
            ),
            0,
            10,
        ),  # Zero radius
        (
            position_global_relative_altitude.PositionGlobalRelativeAltitude.create(3, 6, 12),
            500,
            0,
        ),  # Zero points
    ]

    @pytest.mark.parametrize("result_centre,radius,num_points", invalid_inputs)
    def test_invalid_input(
        self,
        result_centre: (
            tuple[True, position_global_relative_altitude.PositionGlobalRelativeAltitude]
            | tuple[False, None]
        ),
        radius: float,
        num_points: int,
    ) -> None:
        """
        Parameterized test with invalid inputs.
        """
        # Setup
        result, centre = result_centre
        assert result
        assert centre is not None

        # Run
        result, actual = plot_circular_path.generate_circular_path(centre, radius, num_points)

        # Check
        assert not result
        assert actual is None


class TestSaveWaypointsToCsv:
    """
    Test save_waypoints_to_csv function.
    """

    def test_normal(self, tmp_path: pathlib.Path) -> None:
        """
        Save waypoints to a CSV file.
        """
        # Setup
        result, waypoint_0 = (
            position_global_relative_altitude.PositionGlobalRelativeAltitude.create(10, 12, 0)
        )
        assert result
        assert waypoint_0 is not None

        result, waypoint_1 = (
            position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
                10.0001, 12.0001, 0
            )
        )
        assert result
        assert waypoint_1 is not None

        waypoints = [
            waypoint_0,
            waypoint_1,
        ]

        filepath = pathlib.Path(tmp_path, "waypoints.csv")

        # Run
        result = plot_circular_path.save_waypoints_to_csv(waypoints, filepath)

        # Check
        assert result

        with open(filepath, mode="r", encoding="utf-8") as file:
            lines = file.readlines()

        assert lines[0].strip() == "Latitude,Longitude,Altitude"
        assert lines[1].strip() == "10,12,0"
        assert lines[2].strip() == "10.0001,12.0001,0"

    def test_nonexistent_path(self) -> None:
        """
        Fail on nonexistent path.
        """
        # Setup
        result, waypoint_0 = (
            position_global_relative_altitude.PositionGlobalRelativeAltitude.create(10, 12, 0)
        )
        assert result
        assert waypoint_0 is not None

        result, waypoint_1 = (
            position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
                10.0001, 12.0001, 0
            )
        )
        assert result
        assert waypoint_1 is not None

        waypoints = [
            waypoint_0,
            waypoint_1,
        ]

        filepath = pathlib.Path("nonexistent", "waypoints.csv")

        # Run
        result = plot_circular_path.save_waypoints_to_csv(waypoints, filepath)

        # Check
        assert not result
