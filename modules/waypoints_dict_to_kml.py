"""
Module to convert waypoints dict to waypoints list, and generate kml file.
"""
import pathlib

from modules.common.kml.modules.waypoints_to_kml import waypoints_to_kml


def waypoints_dict_to_kml(waypoint_name_to_coordinates: "dict[str, tuple[float, float]]", 
                          document_name: str,
                          save_path: pathlib.Path) -> bool:
    
    """
    Converts dictionary of waypoints into a list and generates a KML file from them.

    Parameters
    ----------
    waypoint_name_to_coordinates: dict[str, tuple[float, float]]]
        Waypoints in key: value form, "waypoint name": (latitude, longitude).
    document_name: str
        Name of the KML file to save (without the .kml extension).
    save_path: pathlib.Path
        Path to save the KML file to.

    Returns
    -------
    bool
        Whether the KML generation was a success.
    """
    
    # create list of all the values in the input dictionary, ie. the tuple[float, float]
    waypoints_list = list(waypoint_name_to_coordinates.values())
    
    # generate kml file in the desired directory and return if successful
    result = waypoints_to_kml(waypoints_list, document_name, save_path)

    return result
