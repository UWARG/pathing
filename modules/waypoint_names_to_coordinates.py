def waypoint_names_to_coordinates(waypoint_names: list[str],
                                  waypoint_mapping: dict[str, tuple[float, float]]) \
        -> tuple[bool, list[tuple[float, float]]]:
    coordinates = []
    for name in waypoint_names:
        if name in waypoint_mapping:
            coordinates.append(waypoint_mapping[name])
        else:
            return False, None
    return True, coordinates

names_valid = ["Waterloo", "Aerial", "Robotics", "Group 15"]
waypoint_dictionary = {
    "Aerial": (9, 7),
    "Group 15": (3, 4),
    "Robotics": (-1, 0),
    "University of Waterloo Station for 301 ION": (6, 6),
    "WARG": (8, 2),
    "Waterloo": (2, -5),
    "Alpha": (),
    "Bravo": (),
    "Charlie": (),
    "Delta": (),
    "Echo": (),
    "Foxtrot": (),
    "Golf": (),
    "Hotel": (),
    "India": (),
    "Juliette": (),
    "Kilo": (),
    "Lima": (),
    "Mike": (),
    "November": (),
    "Oscar": (),
    "Papa": (),
    "Quebec": (),
    "Point 18": (),
    "Romeo": (),
    "Sierra": (),
    "Tango": (),
    "Uniform": (),
    "Victor": (),
    "Whiskey": (),
    "Xray": (),
    "Yankee": (),
    "Zulu": (),
#Added all the waypoint names so it can be used later with the coordinates

}

result, value = waypoint_names_to_coordinates(names_valid, waypoint_dictionary)
print(result)  # True
print(value)  # [(2, -5), (9, 7), (-1, 0), (3, 4)]

names_invalid = ["WARG", "Hello", "World"]

result, value = waypoint_names_to_coordinates(names_invalid, waypoint_dictionary)
print(result)  # False
print(value)  # None
