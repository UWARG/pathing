# """
# Tests functionality for qr_input.
# """

# from modules import qr_input


# CAMERA = 0


# def main() -> int:
#     """
#     Main function.
#     """
#     result, qr_string = qr_input.qr_input(CAMERA)
#     assert result
#     assert qr_string is not None

#     print(f"Decoded QR code with string value: {qr_string}")

#     return 0


# if __name__ == "__main__":
#     result_main = main()
#     if result_main < 0:
#         print(f"ERROR: Status code: {result_main}")

#     print("Done!")
