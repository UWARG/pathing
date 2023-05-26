import cv2
import imutils
from imutils.video import VideoStream
import math
import re

import data_structure_gen
import QR

MAX_PASSENGER = 6 # How many passenger drone can carry
WEIGHT_LIMIT = 1 # How heavy the drone is
OUTPUT_FILE  = "QRpaths.csv"

class QR_CSV:
    def __init__(self):
        self.scanner = QR.QRScanner()
        self.videoStream = VideoStream(src=0).start()
        self.run_video_test()

    def run_video_test(self):
        """
        Runs QR Scanner on live video feed
        """
        output = None

        while True:
            frame = self.videoStream.read()
            frame = imutils.resize(frame)

            frame, output = self.scanner.main(frame)
            cv2.imshow('video', frame)
            key = cv2.waitKey(1) & 0xFF
            if output or key == ord('q'):
                cv2.imwrite("D:/Repositories/WARG/task2-qr.png", frame)
                cv2.destroyAllWindows()
                break
        
        lst = []

        print("Read message from QR:")
        print(output)
        print("")

        for routes in output.split('\n'):
            temp = re.split(":|;", routes)
            if len(temp) < 2:
                continue
            r = re.findall("\d+",temp[1])
            if len(r) > 0:
                if int(r[0]) > MAX_PASSENGER:
                    continue
            r = re.findall("\d+",temp[4])
            if len(r) > 0:
                if WEIGHT_LIMIT > int(r[0]):
                    continue
            # Most disgusting thing ive written in a long time
            lst.append((temp[2].strip()+temp[3].replace(" ",",")+","+re.findall("\d+",temp[6])[0])+','+re.findall("\d+",temp[0])[0])

        coordinates = data_structure_gen.dictionary_imacs("Waypoints_IMACS.csv", True)

        def distance(start: str, end: str, coordinates: dict) -> float:
            return math.hypot(coordinates[end][0] - coordinates[start][0],
                              coordinates[end][1] - coordinates[start][1])

        def high_cost(waypoint_name: str, coordinates: dict) -> float:
            if waypoint_name == "Victor" \
            or waypoint_name == "Uniform" \
            or waypoint_name == "Yankee" \
            or waypoint_name == "Charlie" \
            or waypoint_name == "Kilo" \
            or waypoint_name == "Echo" \
            or waypoint_name == "Romeo":
                return distance("Lima", "Mike", coordinates)

            return 0

        def medium_cost(waypoint_name: str, coordinates: dict) -> float:
            if waypoint_name == "Sierra" \
            or waypoint_name == "Oscar" \
            or waypoint_name == "Zulu" \
            or waypoint_name == "Delta" \
            or waypoint_name == "Mike" \
            or waypoint_name == "Juliette":
                return distance("Lima", "Mike", coordinates) / 2

            return 0

        new_routes_and_cost = []
        for route in lst:
            start, end, _, index = re.split(",", route)
            penalty = max([
                high_cost(start, coordinates),
                high_cost(end, coordinates),
                medium_cost(start, coordinates),
                medium_cost(end, coordinates),
            ])

            penalty += distance(start, end, coordinates)

            new_route = start + "," + end + "," + str(-penalty) + "," + index
            new_routes_and_cost.append(new_route)

        file = open(OUTPUT_FILE, 'w')
        for i in new_routes_and_cost: file.write(i+"\n")
        file.close()
        self.videoStream.stop()