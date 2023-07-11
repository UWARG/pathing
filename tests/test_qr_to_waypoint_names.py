"""
Testcases for parsing QR to waypoint.
"""


from modules.qr_to_waypoint_names import qr_to_waypoint_names


def test_valid_waypoint_single():
    valid, data = qr_to_waypoint_names("Follow route: Alpha")
    assert valid
    assert data == ["Alpha"]

    valid, data = qr_to_waypoint_names("Follow route:    Epsilon      ")
    assert valid
    assert data == ["Epsilon"]

def test_valid_waypoints_multi():
    valid, data = qr_to_waypoint_names("Follow route: Waterloo; Aerial; Robotics; Group 15")
    assert valid
    assert data == ["Waterloo", "Aerial", "Robotics", "Group 15"]

    valid, data = qr_to_waypoint_names("Follow route: A;   B; C,;    D     ")
    assert valid
    assert data == ["A", "B", "C,", "D"]
    
def test_prefix_only():
    valid, data = qr_to_waypoint_names("Follow route: ")
    assert not valid
    assert data is None

    valid, data = qr_to_waypoint_names("Follow route: ; ;   ;   ;")
    assert not valid
    assert data is None

def test_invalid_waypoints():
    valid, data = qr_to_waypoint_names("Avoid the area bounded by: Zulu; Bravo; Tango; Uniform.  Rejoin the route at Lima")
    assert not valid
    assert data is None

    valid, data = qr_to_waypoint_names(" Follow route: A; B; C; D")
    assert not valid
    assert data is None

    valid, data = qr_to_waypoint_names("Follow Route: A; B; C")
    assert not valid
    assert data is None

def test_incorrect_delimiter():
    valid, data = qr_to_waypoint_names("Follow route: A, B, C, D")
    assert valid
    assert data == ["A, B, C, D"]

    valid, data = qr_to_waypoint_names("Follow route: A B C D E F G")
    assert valid
    assert data == ["A B C D E F G"]

    valid, data = qr_to_waypoint_names("Follow route: A: B: C: D:")
    assert valid
    assert data == ["A: B: C: D:"] 
