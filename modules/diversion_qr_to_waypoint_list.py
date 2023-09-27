"""
Function to parse diversion QR string into a list of vertices and a rejoin waypoint.
"""
import re


def diversion_qr_to_waypoint_list(qr_text: str) -> "tuple[bool, tuple[list[str], str] | None]":
    """
    Function for parsing QR text into list of diversion waypoints and a rejoin waypoint.
    Input string format: "Avoid the area bounded by: Name1; Name2; Name3; Name4. Rejoin the route at Waypoint5"

    Parameters
    -----------
    qr_text: str
    Diversion QR string which needs to be parsed.
     
    Returns
    -------
    tuple[bool, tuple[list[Waypoint], Waypoint] | None] 
    Returns False, None if the string is invalid or if the list is empty.
    """
    # Check if string is of valid form
    match = re.search(r"^Avoid the area bounded by:.*\..*Rejoin the route at.*", qr_text)
    if match is None:
        return False, None

    # Separate qr_text into diversion_waypoints and rejoin_waypoint strings
    diversion_waypoints_string, sep, rejoin_waypoint_string = qr_text.partition('.')

    # Extract semicolon-separated list of diversion waypoint names without leading/trailing whitespace
    diversion_waypoints = [
    text.strip(" ") for text in diversion_waypoints_string.replace("Avoid the area bounded by:", "", 1).split(";")
    ]

    # Remove remaining cases of empty names
    filtered = list(filter(lambda text: len(text) > 0, diversion_waypoints))

    # Case of no results
    if len(filtered) == 0:
        return False, None
    
    # Extract rejoin waypoint name, without leading/trailing whitespace
    rejoin_waypoint = (rejoin_waypoint_string.replace("Rejoin the route at", "", 1)).strip()
    
    # Case of rejoin waypoint being empty
    if rejoin_waypoint == "":
        return False, None
    
    return True, (diversion_waypoints, rejoin_waypoint)

