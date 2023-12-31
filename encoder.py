# ChewbaccaBox / Travis 2023
# GORF Controller Image Encoder (.png -> byte array for arduino ide)

import sys
import numpy
from PIL import Image


# Encode each pixel as 2 bits, reading from right to left.
def to_pixel_array(filename):
    array = numpy.array(Image.open(filename).convert('L'))  # Open image, convert to grayscale, put into a NumPy array.
    pixels = []
    for row in array:                               # From top to bottom
        for column in range(row.size - 1, 0, -1):   # From right to left.
            item = row.item(column)                 # Get the pixel at that location.

            if item == 128:          # Border pixels (gray) have a brightness of 128. Skip these.
                pass
            elif item == 76:         # Bright pixels (red) have a brightness of 76. Insert as "10" in array.
                pixels.append("10")
            elif item == 38:         # Dim pixels (dark red) have a brightness of 38. Insert as "01" in array.
                pixels.append("01")
            elif item == 0:          # Off pixels (black) have a brightness of 0. Insert as "00" in array.
                pixels.append("00")
    return pixels


# Put pixel array in terms of bytes & compress large areas of blank space.
def compress_array(pixels):
    current_byte = ""
    compressed = []
    for item in pixels:
        current_byte += item

        if len(current_byte) == 8:
            value = int(current_byte, 2)
            if value == 0:
                if len(compressed) > 0:
                    lastvalue = compressed.pop()
                    if lastvalue[:2] == "11":
                        # The last byte(s) was also straight 0's. So we'll add this to the last byte.
                        num = lastvalue[-4:]
                        if num == "1111":
                            compressed.append(lastvalue)
                            compressed.append("11000001")  # If the last byte is filled up, we'll just start a new one.
                        else:
                            newvalue = "11" + format((int(num, 2) + 1), "b").zfill(6)  # Create new value with last value incremented.
                            compressed.append(newvalue)
                    else:
                        compressed.append(lastvalue)
                        compressed.append("11000001")
                else:
                    compressed.append("11000001")
            else:
                compressed.append(current_byte)
            current_byte = ""
    return compressed


# Output the compressed byte array as a piece of nicely-formatted arduino code.
def pretty_print(compressed, filename):
    # Print variable declaration with variable & comment derived from filename.
    print("const PROGMEM byte frame" + filename[:-4] + "[" + str(len(compressed) + 1) + "]=   // " + filename)
    print("{")

    c = 1
    hexlisting = "\t"   # Start byte data indented.
    for b in compressed:    # Arrange bytes in rows of 10, separated by commas.
        value = hex((int(b, 2))).upper()[2:]
        if len(value) == 1:
            value = "0" + value
        hexlisting += "0x" + value + ", "
        if int(c) % 10 == 0:    # Start a new row at that point.
            hexlisting += "\n\t"
        c += 1;

    # Print size byte, the rest of the byte data, and close the bracket.
    print("\t" + "0x" + hex(len(compressed)).upper()[2:] + ",\t//  Size: " + str(len(compressed) + 1))
    print(hexlisting[:-2])
    print("}; \n")


if __name__ == "__main__":
    print("GORF LED Matrix Image Encoder; Usage: encoder.py filename.png")
    print("Please refer to template.png for a valid input file. \n")

    # Handle file input:
    if len(sys.argv) <= 1 or len(sys.argv) > 2:
        file = input("Enter filename in this directory: ")
    else:
        file = str(sys.argv[1])

    pixels = to_pixel_array(file)
    compressed = compress_array(pixels)
    pretty_print(compressed, file)

    input("Press Enter to close window.")
    sys.exit()


