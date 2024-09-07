"""
Function to read camera input until valid QR code using multithreading.
"""

import threading
import queue
import cv2

from modules.common.qr.modules import qr_scanner
from modules.common.camera.modules import camera_device


def camera_capture_thread(
    device: "int | str",
    frame_queue: queue.Queue,
    stop_event: threading.Event,
) -> None:
    """
    Captures frames from device camera and places into a queue

    Parameters
    ----------
    device: int | string
        Camera device name or index (e.g. /dev/video0).
    frame_queue: queue.Queue
        Queue that stores frames captured by device camera.
    stop_event: threading.Event
        Used to signal the stop of frame capturing.

    Returns
    ----------
    None
    """
    camera = camera_device.CameraDevice(device)
    while not stop_event.is_set():
        is_image_found, frame = camera.get_image()
        if is_image_found:
            frame_queue.put(frame)
        else:
            print("ERROR: Failed to capture image")


def qr_scanner_thread(
    frame_queue: queue.Queue,
    result_queue: queue.Queue,
    stop_event: threading.Event,
    qr_found_event: threading.Event,
) -> None:
    """
    Scans frames for a valid QR code and places the result in a queue

    Parameters
    ----------
    frame_queue: queue.Queue
        Queue that contains frames captured from camera
    result_queue: queue.Queue
        Queue that stores QR scan result.
    stop_event: threading.Event
        Signals when to stop scanning for a QR code
    qr_found_event: threading.Event
        Set when QR code is found.
    """
    scanner = qr_scanner.QrScanner()
    while not stop_event.is_set() and not qr_found_event.is_set():
        if not frame_queue.empty():
            frame = frame_queue.get()
            is_qr_text_found, qr_text = scanner.get_qr_text(frame)
            if is_qr_text_found:
                result_queue.put((is_qr_text_found, qr_text))
                qr_found_event.set()
                stop_event.set()


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

    frame_queue = queue.Queue(maxsize=10)
    result_queue = queue.Queue()
    stop_event = threading.Event()
    qr_found_event = threading.Event()

    grabber_thread = threading.Thread(
        target=camera_capture_thread, args=(device, frame_queue, stop_event)
    )
    scanner_thread = threading.Thread(
        target=qr_scanner_thread, args=(frame_queue, result_queue, stop_event, qr_found_event)
    )

    grabber_thread.start()
    scanner_thread.start()

    is_qr_text_found = False
    qr_text = None

    while not stop_event.is_set():
        if not result_queue.empty():
            is_qr_text_found, qr_text = result_queue.get()
            break

        if not frame_queue.empty():
            frame = frame_queue.get()
            cv2.imshow("Camera", frame)

        if cv2.waitKey(1) == ord("q"):
            stop_event.set()
            break

    grabber_thread.join()
    scanner_thread.join()

    # Cleanup
    cv2.destroyAllWindows()

    if not result_queue.empty():
        is_qr_text_found, qr_text = result_queue.get()

    return is_qr_text_found, qr_text


if __name__ == "__main__":
    device_index = 0
    success, qr_text = qr_input(device_index)
    if success:
        print(f"QR Code detected: {qr_text}")
    else:
        print("No QR Code detected")
