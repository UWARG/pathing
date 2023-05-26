"""
Temporary code for competition 2023
"""
import time


# TODO
BASE_PATH = "TODO: PATH_TO_SOMEWHERE"
LOCATION_FILE = "waypoint_current_location.txt"


while True:
    latitude = cs.lat
    longitude = cs.lng

    output = str(latitude) + "," + str(longitude)

    print("Lat-Lon: " + output)

    output_file = open(BASE_PATH + LOCATION_FILE, "w")
    output_file.write(output)
    output_file.close()

    time.sleep(1)
