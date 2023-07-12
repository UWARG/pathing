"""
Test process
"""

from modules import waypoint_names_to_coordinates

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
}

result, value = waypoint_names_to_coordinates(names_valid, waypoint_dictionary)
print(result)  # True
print(value)  # [(2, -5), (9, 7), (-1, 0), (3, 4)]

names_empty = []
result, value = waypoint_names_to_coordinates(names_empty, waypoint_dictionary)
print(result)  # True
print(value)  # []
