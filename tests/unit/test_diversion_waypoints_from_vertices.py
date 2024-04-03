"""
Test cases for creating waypoints to avoid area bounded by verticies and rejoining path
"""

import pytest

from modules import diversion_waypoints_from_vertices
from modules.common.kml.modules import location_ground
