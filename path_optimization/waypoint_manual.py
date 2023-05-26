
import os

import data_structure_gen
import restriction


WAYPOINT_NAMES_FILE = "Waypoints.csv"
RELATIVE_ALTITUDE = 60  # Metres
MISSION_FILE = "task2_mission.waypoints"
FENCE_FILE = "task2_fence.waypoints"

BUFFER = 0.0001  # Planet Earth degrees (~11 metres)

NON_FLIGHT_AREAS = [
    # Top left
    [
        (48.512416,-71.65284),
        (48.509293,-71.645411),
        (48.504713,-71.647935)
    ],
    # Bottom left
    [
        (48.503332,-71.646455),
        (48.503452,-71.644717),
        (48.503754,-71.643126),
        (48.493829,-71.632581)
    ],
    # Top right
    [
        (48.508742,-71.624235),
        (48.512953,-71.638466),
        (48.513599,-71.639174),
        (48.51422,-71.640021),
        (48.514693,-71.640968),
        (48.515103,-71.64189)
    ]
]


if __name__ == "__main__":
    waypoint_names_to_coordinates = data_structure_gen.dictionary(WAYPOINT_NAMES_FILE, True)

    # 3;4;18;6;7;1;16;9;11;5
    waypoints = [
        "Papa",     #  3
        "Whiskey",  #  4
        "Bravo",    # --
        "Whiskey",  # 18
        "Alpha",    #  6
        "Zulu",     #  7 Hover
        "Alpha",    # --
        "Hotel",    #  1
        "Tango",    # 16
        "Zulu",     #  9 Hover
        "Oscar",    # 11
        "Golf",     #  5
        "Alpha"     # --
    ]

    mission_path = restriction.restriction(waypoint_names_to_coordinates["Alpha"],
                                                 waypoint_names_to_coordinates[waypoints[0]],
                                                 None,
                                                 BUFFER,
                                                 NON_FLIGHT_AREAS)[1:]

    for i in range(1, len(waypoints)):
        if waypoints[i - 1] == "Zulu":
            mission_path.append("loiter")
        else:
            mission_path.append("takeoff")

        path = restriction.restriction(waypoint_names_to_coordinates[waypoints[i - 1]],
                                             waypoint_names_to_coordinates[waypoints[i]],
                                             None,
                                             BUFFER,
                                             NON_FLIGHT_AREAS)

        mission_path += path[1:]

    # Generate mission string
    mission = "QGC WPL 110\n"
    mission += "0\t1\t0\t16\t0\t0\t0\t0\t" + str(waypoint_names_to_coordinates["Alpha"][0]) + "\t" + str(waypoint_names_to_coordinates["Alpha"][1]) + "\t136\t1\n"  # Home
    mission += "1\t0\t3\t17\t0\t0\t0\t0\t0\t0\t0\t1\n"  # TODO: Some takeoff

    # pylint
    for i in range(0, len(mission_path)):
        if mission_path[i] == "takeoff":
            mission += str(i + 2) + "\t0\t3\t17\t0\t0\t0\t0\t0\t0\t0\t1\n"  # TODO: Some takeoff
        elif mission_path[i] == "loiter":
            mission += str(i + 2) + "\t0\t3\t22\t0\t0\t0\t0\t0\t0\t" + str(RELATIVE_ALTITUDE) + "\t1\n"  # TODO: Loiter unlimited
        else:
            # 3 is MAV_FRAME_GLOBAL_RELATIVE_ALT (home altitude = 0)
            # 16 is MAV_CMD_NAV_WAYPOINT
            mission += str(i + 2) + "\t0\t3\t16\t0\t10\t10\tNaN\t" + str(mission_path[i][0]) + "\t" + str(mission_path[i][1]) + "\t" + str(RELATIVE_ALTITUDE) + "\t1\n"

    # VTOL_LAND is failsafe, do not use
    #mission += str(len(mission_path) + 2) + "\t0\t3\t85\t0\t0\t0\t0\t0\t0\t0\t1\n"  # VTOL_LAND
    mission += str(len(mission_path) + 2) + "\t0\t3\t22\t0\t0\t0\t0\t0\t0\t" + str(RELATIVE_ALTITUDE) + "\t1\n"  # TODO: Loiter unlimited

    # Write mission
    base_path = os.path.realpath(os.path.dirname(__file__))
    file_path = base_path + "/" + MISSION_FILE
    output_file = open(file_path, "w")

    print("Writing mission to " + file_path)
    print(mission)

    output_file.write(mission)
    output_file.close()

    print("Done!")
