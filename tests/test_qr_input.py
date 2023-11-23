"""
Tests functionality for qr_input.
"""

from modules import qr_input


CAMERA = 0


if __name__ == '__main__':

    result, qr_string = qr_input.qr_input(CAMERA)
    assert result
    assert qr_string is not None

    print(f"Decoded QR code with string value: {qr_string}")

    print("Done!")
