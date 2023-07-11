import re

def qr_to_waypoint_names(qr_text: str) -> "tuple[bool, list[str] | None]":
    """ Function for parsing QR text into list of waypoints.
    Example of valid string: "Follow route: Waterloo; Aerial; Robotics; Group 15"
    Example of invalid string: "Avoid the area bounded by: Zulu; Bravo; Tango; Uniform.  Rejoin the route at Lima"

    Args:
        qr_text (str): QR Text

    Returns:
        tuple[bool, list[str] | None]: (False, None) if invalid string, (True, data) otherwise
    """
    match = re.search("^Follow route:.*", qr_text)
    if not match:
        return (False, None)
    parsed = [text.strip(" ") for text in qr_text.replace("Follow route:", "", 1).split("; ")]
    return (True, parsed)
