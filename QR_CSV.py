import cv2
import imutils
from imutils.video import VideoStream
import re

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
                cv2.destroyAllWindows()
                break
        
        lst = []

        for routes in output.split('\n'):
            temp = re.split(":|;", routes)
            if int(re.findall("\d+",temp[1])[0]) > MAX_PASSENGER: continue
            if WEIGHT_LIMIT > int(re.findall("\d+",temp[4])[0]) : continue
            # Most disgusting thing ive written in a long time
            lst.append((temp[2].strip()+temp[3].replace(" ",",")+","+re.findall("\d+",temp[6])[0]))

        file = open(OUTPUT_FILE, 'w')
        for i in lst: file.write(i+"\n")
        file.close()
        self.videoStream.stop()