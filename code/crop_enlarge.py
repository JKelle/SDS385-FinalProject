
from PIL import Image
import numpy as np
from scipy.misc import imsave, imread


HAT = [(182, 0), (282, 100)]
SADY_LARS = [(230, 398), (230+80, 398+80)]
BOW = [(201, 5), (201+40, 5+50)]


def enlargeRBG(mat, factor):
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


def showAsImageRGB(mat):
    img = Image.fromarray(mat, 'RGB')
    img.show()



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


def main():
    origColor()
    origGray()


if __name__ == '__main__':
    main()
