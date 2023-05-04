"""
Temporary code for competition 2023
"""
import os
import re

import cv2

import data_structure_gen
import QR


CAMERA = 0
WAYPOINT_NAMES_FILE = "waypoint_test_points.csv"
RELATIVE_ALTITUDE = 20  # Metres TODO: Is this good?
MISSION_FILE = "mission.waypoints"

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

    mission = "QGC WPL 110\n"
    # TODO: Home lat lon alt
    mission += "0\t1\t0\t16\t0\t0\t0\t0\t48.5084877\t-71.6480041\t128\t1\n"  # Home
    mission += "1\t0\t3\t84\t0\t0\t0\t0\t0\t0\t0\t1\n"  # VTOL_TAKEOFF

    waypoint_names_to_coordinates = data_structure_gen.dictionary(WAYPOINT_NAMES_FILE, True)
    waypoints = output.split("; ")
    index = 2
    for waypoint_name in waypoints:
        latitude = waypoint_names_to_coordinates[waypoint_name][0]
        longitude = waypoint_names_to_coordinates[waypoint_name][1]

        # 3 is MAV_FRAME_GLOBAL_RELATIVE_ALT (home altitude = 0)
        # 16 is MAV_CMD_NAV_WAYPOINT
        mission += str(index) + "\t0\t3\t16\t0\t10\t10\tNaN\t" + str(latitude) + "\t" + str(longitude) + "\t" + str(RELATIVE_ALTITUDE) + "\t1\n"
        index += 1

    mission += str(index) + "\t0\t3\t85\t0\t0\t0\t0\t0\t0\t0\t1\n"  # VTOL_LAND

    # Write mission
    base_path = os.path.realpath(os.path.dirname(__file__))
    output_file = open(base_path + "/" + MISSION_FILE, "w")
    output_file.write(mission)
    output_file.close()

    print("Done!")
