"""
Test plotting waypoints in a circular fashion around a center
"""

from modules import plot_circular_path
from modules.waypoint import Waypoint


def assert_close_enough(point_1: Waypoint, point_2: Waypoint, epsilon: float = 1e-7) -> bool:
    """
    Assert whether two waypoints are within epsilon within each other, in both
    the x and y directions.
    A default epsilon of 1e-7 was chosen so that any error within that range is
    within an error of 1.1 centimeter.
    """
    return (
        abs(point_1.location_ground.latitude - point_2.location_ground.latitude) < epsilon
        and abs(point_1.location_ground.longitude - point_2.location_ground.longitude) < epsilon
        and abs(point_1.altitude - point_2.altitude) < epsilon
    )


def test_move_north_east() -> None:
    """
    Move the drone north east
    """
    starting_point = Waypoint("Start", 10, 12, 1)
    offset_x = 100_000  # east
    offset_y = 100_000  # north
    expected_point = Waypoint("End", 10.899322, 12.913195, 1)

    result_point = plot_circular_path.move_coordinates_by_offset(
        starting_point, offset_x, offset_y, "End"
    )

    print(f"result_point: {result_point}")

    assert_close_enough(result_point, expected_point)


def test_generate_circular_path() -> None:
    """
    Generate a circular path
    """
    center = Waypoint("Center", 10, 12, 1)
    radius = 1_000_000
    num_points = 20
    waypoints = plot_circular_path.generate_circular_path(center, radius, num_points)

    expected_points = [
        (10.0, 21.131950912937036),
        (12.77905659637457, 20.685001422236247),
        (15.286079770270131, 19.387903480363878),
        (17.275664625968226, 17.367626071283176),
        (18.55305673554031, 14.82192802389536),
        (18.993216059187304, 12.0),
        (18.55305673554031, 9.17807197610464),
        (17.275664625968226, 6.632373928716825),
        (15.286079770270131, 4.612096519636122),
        (12.779056596374572, 3.3149985777637543),
        (10.0, 2.868049087062964),
        (7.220943403625431, 3.3149985777637543),
        (4.71392022972987, 4.612096519636121),
        (2.724335374031777, 6.632373928716823),
        (1.4469432644596925, 9.178071976104638),
        (1.006783940812694, 12.0),
        (1.4469432644596907, 14.821928023895358),
        (2.724335374031776, 17.367626071283176),
        (4.713920229729867, 19.387903480363878),
        (7.220943403625428, 20.685001422236247),
    ]

    assert len(waypoints) == num_points

    for i in range(num_points):
        assert_close_enough(
            waypoints[i], Waypoint(f"Waypoint {i}", expected_points[i][0], expected_points[i][1], 1)
        )


def test_save_waypoints_to_csv(tmp_path: str) -> None:
    """
    Save waypoints to a CSV file
    """
    waypoints = [
        Waypoint("WP1", 10, 12, 0),
        Waypoint("WP2", 10.0001, 12.0001, 0),
    ]
    filename = tmp_path / "waypoints.csv"
    plot_circular_path.save_waypoints_to_csv(waypoints, filename)

    with open(filename, mode="r", encoding="UTF-8") as file:
        lines = file.readlines()

    assert lines[0].strip() == "Name,Latitude,Longitude,Altitude"
    assert lines[1].strip() == "WP1,10,12,0"
    assert lines[2].strip() == "WP2,10.0001,12.0001,0"
