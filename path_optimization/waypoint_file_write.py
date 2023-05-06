"""
Temporary code for competition 2023
"""
import os
import re

import cv2

import data_structure_gen
import QR
import restriction


CAMERA = 0

WAYPOINT_NAMES_FILE = "Waypoints.csv"
RELATIVE_ALTITUDE = 60  # Metres
MISSION_FILE = "mission.waypoints"

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
    camera = cv2.VideoCapture(CAMERA)
    scanner = QR.QRScanner()
    while True:
        result, image = camera.read()
        if not result:
            continue

        cv2.imshow('video', image)

        _, output = scanner.main(image)
        if output is not None:
            cv2.destroyAllWindows()
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    # Debugging
    print(output)

    # TODO
    is_path = True
    if re.search("Avoid", output):
        output = output.replace("Avoid the area bounded by: ", "")
        output = output.replace(".  Rejoin the route at", ";")
        is_path = False
    else:
        output = output.replace("Follow route: ", "")

    waypoint_names_to_coordinates = data_structure_gen.dictionary(WAYPOINT_NAMES_FILE, True)

    waypoints = output.split("; ") + ["Alpha"]
    mission_path = restriction.restriction(waypoint_names_to_coordinates["Alpha"],
                                                 waypoint_names_to_coordinates[waypoints[0]],
                                                 None,
                                                 BUFFER,
                                                 NON_FLIGHT_AREAS)[1:]
    print(len(mission_path))

    for i in range(1, len(waypoints)):
        path = restriction.restriction(waypoint_names_to_coordinates[waypoints[i - 1]],
                                             waypoint_names_to_coordinates[waypoints[i]],
                                             None,
                                             BUFFER,
                                             NON_FLIGHT_AREAS)

        print(len(path))
        mission_path += path[1:]

    print(len(mission_path))

    # Generate mission string
    mission = "QGC WPL 110\n"
    mission += "0\t1\t0\t16\t0\t0\t0\t0\t" + str(waypoint_names_to_coordinates["Alpha"][0]) + "\t" + str(waypoint_names_to_coordinates["Alpha"][1]) + "\t136\t1\n"  # Home
    mission += "1\t0\t3\t84\t0\t0\t0\t0\t0\t0\t" + str(RELATIVE_ALTITUDE) + "\t1\n"  # VTOL_TAKEOFF

    for i in range(0, len(mission_path)):
        # 3 is MAV_FRAME_GLOBAL_RELATIVE_ALT (home altitude = 0)
        # 16 is MAV_CMD_NAV_WAYPOINT
        mission += str(i + 2) + "\t0\t3\t16\t0\t10\t10\tNaN\t" + str(mission_path[i][0]) + "\t" + str(mission_path[i][1]) + "\t" + str(RELATIVE_ALTITUDE) + "\t1\n"

    mission += str(len(mission_path) + 2) + "\t0\t3\t85\t0\t0\t0\t0\t0\t0\t0\t1\n"  # VTOL_LAND

    # Write mission
    base_path = os.path.realpath(os.path.dirname(__file__))
    output_file = open(base_path + "/" + MISSION_FILE, "w")
    output_file.write(mission)
    output_file.close()

    print("Done!")
