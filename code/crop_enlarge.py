
"""
This module crops the full-resolution image to the two examples shown in the
paper: the girls bow and the characters exiting the donut shop. This script
also enlarges the cropped photos to make the pixels easier to see.

This script is run separately from experiments.py.
"""

import numpy as np
from scipy.misc import imsave, imread


# bounding box cooridinates for different regions of interest
HAT = [(182, 0), (282, 100)]
SADY_LARS = [(230, 398), (230+80, 398+80)]
BOW = [(201, 5), (201+40, 5+50)]


def enlargeRBG(mat, factor):
    """
    Enlarges the image by a factor of `factor` in both (x and y) directions.
    Works by copying each pixel value `factor` times in each direction.

    For color images with 3 channels.

    Args:
        mat: image to enlarge (3D numpy array)
        factor: int >= 1

    Returns:
        mat2: the enlarged image (3D numpy array)
    """
    assert factor >= 1
    assert type(factor) is int
    assert len(mat.shape) == 3

    orig_height, orig_width, num_channels = mat.shape
    assert num_channels == 3

    new_width = orig_width * factor
    new_height = orig_height * factor
    mat2 = np.zeros((new_height, new_width, num_channels), dtype='uint8')

    for y in range(orig_height):
        for x in range(orig_width):
            # copy the original pixel from mat to the new, larger region in mat2
            mat2[y*factor:(y+1)*factor, x*factor:(x+1)*factor, :] = mat[y, x, :]

    return mat2


def enlargeGray(mat, factor):
    """
    Enlarges the image by a factor of `factor` in both (x and y) directions.
    Works by copying each pixel value `factor` times in each direction.

    For grayscale images with 1 channel.

    Args:
        mat: image to enlarge (2D numpy array)
        factor: int >= 1

    Returns:
        mat2: the enlarged image (2D numpy array)
    """
    assert factor >= 1
    assert type(factor) is int
    assert len(mat.shape) == 2

    orig_height, orig_width = mat.shape

    new_width = orig_width * factor
    new_height = orig_height * factor
    mat2 = np.zeros((new_height, new_width), dtype='uint8')

    for y in range(orig_height):
        for x in range(orig_width):
            # copy the original pixel from mat to the new, larger region in mat2
            mat2[y*factor:(y+1)*factor, x*factor:(x+1)*factor] = mat[y, x]

    return mat2


########################################################################
#  runs the crop/enlarge operations on different sets of input images  #
########################################################################


def origColor():
    filename = "../data/cartoon/colorFrames/colorFrame000300.jpg"
    img = imread(filename)

    # crop hat
    (y1, x1), (y2, x2) = HAT
    cropimg = img[y1:y2, x1:x2, :]
    largeimg = enlargeRBG(cropimg, 10)
    imsave("../data/cartoon/colorFrames/hat_large.bmp", largeimg)
    imsave("../data/cartoon/colorFrames/hat.bmp", cropimg)

    # crop bow
    (y1, x1), (y2, x2) = BOW
    cropimg = img[y1:y2, x1:x2, :]
    largeimg = enlargeRBG(cropimg, 10)
    imsave("../data/cartoon/colorFrames/bow_large.bmp", largeimg)
    imsave("../data/cartoon/colorFrames/bow.bmp", cropimg)

    # crop sady_lars
    (y1, x1), (y2, x2) = SADY_LARS
    cropimg = img[y1:y2, x1:x2, :]
    largeimg = enlargeRBG(cropimg, 10)
    imsave("../data/cartoon/colorFrames/sady_lars_large.bmp", largeimg)
    imsave("../data/cartoon/colorFrames/sady_lars.bmp", cropimg)


def origGray():
    filename = "../data/cartoon/grayFrames/grayFrame000300.jpg"
    img = imread(filename)

    # crop hat
    (y1, x1), (y2, x2) = HAT
    cropimg = img[y1:y2, x1:x2]
    largeimg = enlargeGray(cropimg, 10)
    imsave("../data/cartoon/grayFrames/hat_large.bmp", largeimg)
    imsave("../data/cartoon/grayFrames/hat.bmp", cropimg)

    # crop bow
    (y1, x1), (y2, x2) = BOW
    cropimg = img[y1:y2, x1:x2]
    largeimg = enlargeGray(cropimg, 10)
    imsave("../data/cartoon/grayFrames/bow_large.bmp", largeimg)
    imsave("../data/cartoon/grayFrames/bow.bmp", cropimg)

    # crop sady_lars
    (y1, x1), (y2, x2) = SADY_LARS
    cropimg = img[y1:y2, x1:x2]
    largeimg = enlargeGray(cropimg, 10)
    imsave("../data/cartoon/grayFrames/sady_lars_large.bmp", largeimg)
    imsave("../data/cartoon/grayFrames/sady_lars.bmp", cropimg)


def alphaResults():
    filenames = [
        ("/Users/jkelle/Desktop/StatsProject/results/cartoon/color/transfered_050_001_13.bmp", 50),
        ("/Users/jkelle/Desktop/StatsProject/results/cartoon/color/transfered_100_001_13.bmp", 100),
        ("/Users/jkelle/Desktop/StatsProject/results/cartoon/color/transfered_200_001_10.bmp", 200),
        ("/Users/jkelle/Desktop/StatsProject/results/cartoon/color/transfered_400_001_09.bmp", 400),
        ("/Users/jkelle/Desktop/StatsProject/results/cartoon/color/transfered_800_001_11.bmp", 800),
        ("/Users/jkelle/Desktop/StatsProject/results/cartoon/color/transfered_1600_001_10.bmp", 1600),
    ]
    for filename, ind in filenames:
        img = imread(filename)

        path = "/Users/jkelle/Desktop/StatsProject/results/cartoon/color/%s_%04d.bmp"

        # crop hat
        (y1, x1), (y2, x2) = HAT
        cropimg = img[y1:y2, x1:x2]
        largeimg = enlargeRBG(cropimg, 10)
        imsave(path % ("hat_large", ind), largeimg)
        imsave(path % ("hat", ind), cropimg)

        # crop bow
        (y1, x1), (y2, x2) = BOW
        cropimg = img[y1:y2, x1:x2]
        largeimg = enlargeRBG(cropimg, 10)
        imsave(path % ("bow_large", ind), largeimg)
        imsave(path % ("bow", ind), cropimg)

        # crop sady_lars
        (y1, x1), (y2, x2) = SADY_LARS
        cropimg = img[y1:y2, x1:x2]
        largeimg = enlargeRBG(cropimg, 10)
        imsave(path % ("sadylars_large", ind), largeimg)
        imsave(path % ("sadylars", ind), cropimg)


def gradminResults():
    filenames = [
        ("/Users/jkelle/Desktop/StatsProject/results/cartoon/color/gradmin_0.0010_1.10_.bmp", 1),
        ("/Users/jkelle/Desktop/StatsProject/results/cartoon/color/gradmin_0.0020_1.10_.bmp", 2),
        ("/Users/jkelle/Desktop/StatsProject/results/cartoon/color/gradmin_0.0040_1.10_.bmp", 4),
        ("/Users/jkelle/Desktop/StatsProject/results/cartoon/color/gradmin_0.0080_1.10_.bmp", 8),
        ("/Users/jkelle/Desktop/StatsProject/results/cartoon/color/gradmin_0.0160_1.10_.bmp", 16),
        ("/Users/jkelle/Desktop/StatsProject/results/cartoon/color/gradmin_0.0320_1.10_.bmp", 32),
    ]
    for filename, ind in filenames:
        img = imread(filename)

        path = "/Users/jkelle/Desktop/StatsProject/results/cartoon/color/gradmin_%s_%04d.bmp"

        # crop hat
        (y1, x1), (y2, x2) = HAT
        cropimg = img[y1:y2, x1:x2]
        largeimg = enlargeRBG(cropimg, 10)
        imsave(path % ("hat_large", ind), largeimg)
        imsave(path % ("hat", ind), cropimg)

        # crop bow
        (y1, x1), (y2, x2) = BOW
        cropimg = img[y1:y2, x1:x2]
        largeimg = enlargeRBG(cropimg, 10)
        imsave(path % ("bow_large", ind), largeimg)
        imsave(path % ("bow", ind), cropimg)

        # crop sady_lars
        (y1, x1), (y2, x2) = SADY_LARS
        cropimg = img[y1:y2, x1:x2]
        largeimg = enlargeRBG(cropimg, 10)
        imsave(path % ("sadylars_large", ind), largeimg)
        imsave(path % ("sadylars", ind), cropimg)


##########
#  main  #
##########


def main():
    # origColor()
    # origGray()
    # alphaResults()
    gradminResults()


if __name__ == '__main__':
    main()
