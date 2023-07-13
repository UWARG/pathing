"""
Function to read camera input until valid QR code
"""

from common.qr.modules import qr_scanner
from common.camera.modules import camera_device


def qr_input(device: "int | string") -> str:
    """
    Checks camera input indefinitely until valid text is decoded from QR code.

    Parameters
    ----------
    device: int | string
        Camera device name or index (e.g. /dev/video0).

    Returns
    -------
    str
        Decoded QR code string.
    """
    camera = camera_device.CameraDevice(device)
    scanner = qr_scanner.QrScanner()

    qr_text_found = False
    qr_text = None
    while not qr_text_found:
        # Get new image from camera as long as QR text not found
        image_found, frame = camera.get_image()

        if image_found:
            # Check frame for valid QR code if found
            qr_text_found, qr_text = scanner.get_qr_text(frame)

        if qr_text_found:
            # Exit and return decoded text if found
            return qr_text
