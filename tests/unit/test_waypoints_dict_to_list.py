"""
Testing various formats of waypoints dictionary during conversion to list process.
"""

from modules import waypoints_dict_to_list
from modules.common.modules import location_global
from modules.common.modules import position_global_relative_altitude


# Test functions use test fixture signature names and access class privates
# No enable
# pylint: disable=protected-access,redefined-outer-name


class TestWaypointsDict:
    """
    No altitude.
    """

    def test_valid(self) -> None:
        """
        Test conversion to list for a valid map.
        """
        # Setup
        name_alpha = "Alpha"
        result, alpha = location_global.LocationGlobal.create(43.4340501, -80.5789803)
        assert result
        assert alpha is not None

        name_bravo = "Bravo"
        result, bravo = location_global.LocationGlobal.create(43.4335758, -80.5775237)
        assert result
        assert bravo is not None

        name_charlie = "Charlie"
        result, charlie = location_global.LocationGlobal.create(43.4336672, -80.57839)
        assert result
        assert charlie is not None

        waypoint_mapping = {name_alpha: alpha, name_bravo: bravo, name_charlie: charlie}

        expected = [alpha, bravo, charlie]

        # Run
        result, actual = waypoints_dict_to_list.waypoints_dict_to_list(waypoint_mapping)

        # Check
        assert result
        assert actual == expected

    def test_empty(self) -> None:
        """
        Test conversion to list for an empty map.
        """
        # Setup
        waypoint_mapping = {}

        # Run
        result, actual = waypoints_dict_to_list.waypoints_dict_to_list(waypoint_mapping)

        # Check
        assert not result
        assert actual is None


class TestWaypointsDictWithAltitude:
    """
    With altitude.
    """

    def test_valid(self) -> None:
        """
        Test conversion to list for a valid map.
        """
        # Setup
        name_alpha = "Alpha"
        result, alpha = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
            43.4340501, -80.5789803, 10.0
        )
        assert result
        assert alpha is not None

        name_bravo = "Bravo"
        result, bravo = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
            43.4335758, -80.5775237, 10.0
        )
        assert result
        assert bravo is not None

        name_charlie = "Charlie"
        result, charlie = position_global_relative_altitude.PositionGlobalRelativeAltitude.create(
            43.4336672, -80.57839, 10.0
        )
        assert result
        assert charlie is not None

        waypoint_mapping = {name_alpha: alpha, name_bravo: bravo, name_charlie: charlie}
        expected = [alpha, bravo, charlie]

        # Run
        result, actual = waypoints_dict_to_list.waypoints_dict_with_altitude_to_list(
            waypoint_mapping
        )

        # Check
        assert result
        assert actual == expected

    def test_empty(self) -> None:
        """
        Test conversion to list for an empty map.
        """
        # Setup
        waypoint_mapping = {}

        # Run
        result, actual = waypoints_dict_to_list.waypoints_dict_with_altitude_to_list(
            waypoint_mapping
        )

        # Check
        assert not result
        assert actual is None
