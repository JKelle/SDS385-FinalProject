
"""
Print out pixels values of a color Image.

Output from this program is piped to smoothColor.cpp.
This file exists because I couldn't get openCV to compile for smoothColor.cpp.
It is a hacky wait to load the image into smoothColor.cpp.
"""

import os
from PIL import Image

ROOT_DIR = "/Users/jkelle/Desktop/StatsProject"

img = Image.open(os.path.join(ROOT_DIR, 'data/cartoon/colorFrames/colorFrame000300.jpg'))
width, height = img.size

for y in range(height):
    for x in range(width):
        for pixel in img.getpixel((x, y)):
            print pixel
