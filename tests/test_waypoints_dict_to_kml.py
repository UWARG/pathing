"""
Test Process.
"""

import pytest
import pathlib

from modules import waypoints_dict_to_kml

@pytest.fixture
def waypoints():
    return {"Alpha": (43.4340501,-80.5789803), "Bravo": (43.4335758,-80.5775237), "Charlie": (43.4336672,-80.57839)}


def test_waypoints_dict_to_kml(waypoints: "dict[str, tuple[float, float]]"):
    """
    Basic test case to see if KML file is generated from a dictionary of waypoints.
    """

    # name and directory for testing purposes
    test_document_name = "test_kml_document"
    test_path = pathlib.Path(".", "tests", "test_kml")

    # determine if action was successful
    result = waypoints_dict_to_kml.waypoints_dict_to_kml(waypoints, test_document_name, test_path)

    assert result
