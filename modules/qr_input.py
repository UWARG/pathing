"""
Function to read camera input until valid QR code.
"""

import cv2

from modules.common.qr.modules import qr_scanner
from modules.common.camera.modules import camera_device


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
    camera = camera_device.CameraDevice(device)
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
        if cv2.waitKey(1) == ord('q'):
            break

    # Cleanup
    cv2.destroyAllWindows()

    return is_qr_text_found, qr_text
