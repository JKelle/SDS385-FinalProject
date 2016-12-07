
"""
Print out pixels values of a grayscale Image.

Output from this program is piped to smoothGray.cpp.
This file exists because I couldn't get openCV to compile for smoothGray.cpp.
It is a hacky wait to load the image into smoothGray.cpp.
"""

from PIL import Image

img = Image.open('../data/cartoon/grayFrames/grayFrame000300.jpg')
width, height = img.size

for y in range(height):
    for x in range(width):
        print img.getpixel((x, y))
