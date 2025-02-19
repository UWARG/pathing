"""
Function to read camera input until valid QR code.
"""

import cv2

from modules.common.modules.camera import camera_factory
from modules.common.modules.qr import qr_scanner

CAMERA_WIDTH = 1920
CAMERA_HEIGHT = 1080


def diversion_qr_input(device: "int | str") -> "tuple[bool, str | None]":
    """
    Checks camera input once, returns any valid text that is decoded from QR code.

    Parameters
    ----------
    device: int | string
        Camera device name or index (e.g. /dev/video0).

    Returns
    -------
    tuple[bool, str | None]
        A tuple indicating the success of the operation and the decoded QR code string, or None if unsuccessful.
    """
    camera = camera_factory.create_camera(
        camera_factory.CameraOption.OPENCV,
        CAMERA_WIDTH,
        CAMERA_HEIGHT,
        camera_factory.camera_opencv.ConfigOpenCV(device),
    )
    scanner = qr_scanner.QrScanner()

    qr_text = None
    is_qr_text_found = False

    # Get new image from camera as long as QR text not found
    is_image_found, frame = camera.get_image()

    if not is_image_found:
        # Log error is camera fails to get image
        print("ERROR: is_image_found returned false. Cannot get image from camera")
    else:
        cv2.imshow("Camera", frame)

        # Check frame for valid QR code if found
        is_qr_text_found, qr_text = scanner.get_qr_text(frame)

    # Cleanup
    cv2.destroyAllWindows()

    return is_qr_text_found, qr_text
