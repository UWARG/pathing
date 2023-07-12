"""
Module to parse QR string to waypoints.
"""
import re


def qr_to_waypoint_names(qr_text: str) -> "tuple[bool, list[str] | None]":
    """ 
    Function for parsing QR text into list of waypoints.
    Example of valid string: "Follow route: Waterloo; Aerial; Robotics; Group 15"
    Example of invalid string: "Avoid the area bounded by: Zulu; Bravo; Tango; Uniform.  Rejoin the route at Lima"

    Args:
        qr_text (str): QR Text

    Returns:
        tuple[bool, list[str] | None]: (False, None) if invalid string or no results, (True, data) otherwise
    """
    match = re.search("^Follow route:.*", qr_text)
    if match is None:
        return False, None

    # Extract semicolon-separated list of waypoint names without leading/trailing whitespace
    parsed = [text.strip(" ") for text in qr_text.replace("Follow route:", "", 1).split(";")]

    # Remove remaining cases of empty names
    filtered = list(filter(lambda text: len(text) > 0, parsed))

    # Case of no results
    if len(filtered) == 0:
        return False, None
    
    return True, filtered
