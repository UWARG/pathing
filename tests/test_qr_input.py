"""
Test process.
"""
import pytest

from modules import qr_input


CAMERA = 0


pytest.skip("Integration test", allow_module_level=True)


def test_qr_input():
    """
    Tests functionality for qr_input
    """
    is_qr_found, qr_string = qr_input.qr_input(CAMERA)

    if is_qr_found:
        print(f"Decoded QR code with string value: {qr_string}")
    else:
        print("Exited early before a QR code was read")


if __name__ == '__main__':
    test_qr_input()
