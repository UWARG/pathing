import cv2
import imutils
from imutils.video import VideoStream
import data_structure_gen
import time
import re

from pyzbar import pyzbar

import QR
import restriction


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


class PathOptim:
    """
    Unit Tests for QR.py
    ...

    Attributes
    ----------
    scanner : QRScanner
        QR.py module
    videoStream : imutils.video.VideoStream
        Incoming video to be read

    Methods
    -------
    __init__()
        Initializes module, runs single image test & video test
    run_single_image_test(imagePath : str)
        Runs QR Scanner on a single, static image
    run_video_test()
        Runs QR Scanner on live video feed
    """

    def __init__(self):
        """
        Initializes module, runs single image test & video test
        """

        self.thisdict = data_structure_gen.dictionary("Waypoints.csv", True)
        self.scanner = QR.QRScanner()
        self.node_list = []
        # imagePath = "task1QR1.png"
        # self.run_single_image_test(imagePath)

        self.videoStream = VideoStream(src=0).start()
        self.run_video_test()
        

    def run_single_image_test(self, imagePath):
        """
        Runs QR Scanner on a single, static image

        Parameters
        ----------
        imagePath : str
            Relative path to the image to be tested
        """
        image = cv2.imread(imagePath)
        image, output = self.scanner.main(image)

    def update_path_file(self, output_list):
        '''
        Update the paths.txt file (Be sure to change the pathing depending on device)
        '''
        if(output_list[0] == True): # Normal route
            for i in output_list[1]:
                self.node_list.append(i[1])
        else: # Diversion route
            start = (48.504569,-71.646339) # Need to figure out how we can get this information
            end = output_list[1][-1][1]
            bound = []
            for i in range(0,len(output_list[1])-1):
                bound.append(
                    output_list[1][i][1]
                )
            # remember to pass in UTM coordinates, or set up a checker in the restriction function
            a = restriction.restriction(start, end, bound, BUFFER, NON_FLIGHT_AREAS)
            print("Restriction:")
            print(a)
        
        print(self.node_list)

        # CHANGE THE FILE PATH TO paths.txt HERE. USE THE ABSOLUTE PATH
        filename = "D:/Repositories/WARG/IMACS/path_optimization/paths.txt"
        output_file = open(filename, 'w')
        output_file.write(str(self.node_list))
        
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

        ispath = True
        if re.search("Avoid", output):
            output = output.replace("Avoid the area bounded by: ", "")
            output = output.replace(".  Rejoin the route at", ";")
            ispath = False
        else:
            output = output.replace("Follow route: ", "")

        output_list = (ispath, [(element, self.thisdict[element]) for element in output.split("; ")])
        print(output_list)
        self.update_path_file(output_list)
        
        self.videoStream.stop()
    

if __name__ == "__main__":
    PathOptim()