"""
Test process
"""

from modules import qr_input

CAMERA = 1


def test_qr_input():
    """
    Tests functionality for qr_input
    """
    is_qr_found, qr_string = qr_input.qr_input(CAMERA)

    if is_qr_found:
        print(f'Decoded QR code with string value: {qr_string}')
    else:
        print('Exited early before a QR code was read')
