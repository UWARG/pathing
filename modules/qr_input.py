"""
Function to read camera input until valid QR code.
"""

import cv2

from .common.modules.camera import camera_factory
from .common.modules.qr import qr_scanner

CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080


def qr_input(device: "int | str") -> "tuple[bool, str | None]":
    """
    Checks camera input indefinitely until valid text is decoded from QR code.

    Parameters
    ----------
    device: int | string
        Camera device name or index (e.g. /dev/video0).

    Returns
    -------
    tuple[bool, str | None]
        A tuple indicating the success of the operation and the decoded QR code string, or None if unsuccessful.
    """
    # Camera also created in diversion_qr_input.py with similar code, hence the the next to make pylint shut up
    # pylint: disable=duplicate-code
    result, camera = camera_factory.create_camera(
        camera_factory.CameraOption.OPENCV,
        CAMERA_WIDTH,
        CAMERA_HEIGHT,
        camera_factory.camera_opencv.ConfigOpenCV(device),
    )
    if not result:
        print("OpenCV camera creation error.")
        return False, None
    # pylint: enable=duplicate-code

    scanner = qr_scanner.QrScanner()

    is_qr_text_found = False
    qr_text = None
    while not is_qr_text_found:
        # Get new image from camera as long as QR text not found
        is_image_found, frame = camera.get_image()
        if not is_image_found:
            # Log error is camera fails to get image
            print("ERROR: is_image_found returned false. Cannot get image from camera")
            continue

        cv2.imshow("Camera", frame)

        if is_image_found:
            # Check frame for valid QR code if found
            is_qr_text_found, qr_text = scanner.get_qr_text(frame)

        if is_qr_text_found:
            break

        # Exit early on manual quit
        if cv2.waitKey(1) == ord("q"):
            break

    # Cleanup
    cv2.destroyAllWindows()

    return is_qr_text_found, qr_text
