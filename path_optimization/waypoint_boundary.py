"""
Temporary code for competition 2023
"""
import os
import re

import cv2

import data_structure_gen
import QR


CAMERA = 0

WAYPOINT_NAMES_FILE = "Waypoints.csv"
FENCE_FILE = "fence.waypoints"


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
    waypoints = output.split("; ")

    boundary = waypoints[0:4]
    rejoin = waypoints[4]

    # Generate fence string
    fence = "QGC WPL 110\n"
    fence += "0\t0\t0\t16\t0\t0\t0\t0\t" + str(waypoint_names_to_coordinates["Alpha"][0]) + "\t" + str(waypoint_names_to_coordinates["Alpha"][1]) + "\t136\t1\n"  # Home

    for i in range(0, 4):
        fence += str(i + 1) + "\t0\t4\t5002\t4\t0\t0\t0\t" + str(waypoint_names_to_coordinates[boundary[i]][0]) + "\t" + str(waypoint_names_to_coordinates[boundary[i]][1]) + "\t" + str(i) + "\t1\n"

    # Write fence
    base_path = os.path.realpath(os.path.dirname(__file__))
    output_file = open(base_path + "/" + FENCE_FILE, "w")
    output_file.write(fence)
    output_file.close()

    print("Done!")
