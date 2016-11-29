
"""
Print out pixels values of a grayscale Image.

Output from this program is piped to main.cpp.
This file exists because I couldn't get openCV to compile for main.cpp.
"""

from PIL import Image

img = Image.open('../data/cartoon/grayFrames/grayFrame000300.jpg')
width, height = img.size

for y in range(height):
    for x in range(width):
        print img.getpixel((x, y))
