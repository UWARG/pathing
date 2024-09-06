import cv2
import threading
import queue

from common.qr.modules import qr_scanner
from common.camera.modules import camera_device


def camera_capture_thread(
    device: "int | str",
    frame_queue: queue.Queue,
    stop_event: threading.Event,
) -> None:
    camera = camera_device.CameraDevice(device)
    while not stop_event.is_set():
        is_image_found, frame = camera.get_image()
        if is_image_found:
            if frame_queue.full():
                frame_queue.get()
            frame_queue.put(frame)
        else:
            print("ERROR: Failed to capture image")


def qr_scanner_thread(
    frame_queue: queue.Queue,
    result_queue: queue.Queue,
    stop_event: threading.Event,
    qr_found_event: threading.Event,
) -> None:
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
