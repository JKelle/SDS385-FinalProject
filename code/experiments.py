
"""
This module is the main driver for running alpha-expansion across several values
of lambda. It relies on the ./smoothGray binary, which in turn depends on the
gco-v3.0 library.
The ./smoothGray binary can be compiled with the following command:
    `g++ gco-v3.0/smoothGray.cpp  gco-v3.0/GCoptimization.cpp gco-v3.0/graph.cpp gco-v3.0/LinkedBlockList.cpp gco-v3.0/maxflow.cpp -o smoothGray`
"""

import os
import subprocess
import numpy as np
from scipy.misc import imsave, imread
from PIL import Image


WIDTH = 640
HEIGHT = 360

ROOT_DIR = "/Users/jkelle/Desktop/StatsProject"


############################################
#  run alpha-expansion on grayscale image  #
############################################


def runOptimization(lambda1, lambda2, max_cycles):
    """
    Invokes alpha-expansion. Runs the binary smoothGray in a child process.
    To compile the C++ binary: `g++ gco-v3.0/smoothGray.cpp  gco-v3.0/GCoptimization.cpp gco-v3.0/graph.cpp gco-v3.0/LinkedBlockList.cpp gco-v3.0/maxflow.cpp -o smoothGray`

    The smoothness cost function V is defined as:
        V(u, v) = lambda1 * min(lambda2, |u - v|)
    If lambda1 == lambda2 == 1, this is the Potts Model.

    Args:
        lambda1: (int > 0) as defined above
        lambda2: (int > 0) as defined above
        max_cycles: (int) the max number of alpha-expansion cycles to run.
            For the example cartoon image in my paper, this usually converges
            after about 11 cycles.

    This binary serializes the smoothed image to a .txt file defined by the src_path_pattern
    variable in main().
    """
    command = "python cat_image.py | ./smoothGray %i %i %i" % (lambda1, lambda2, max_cycles)
    print "command:", command
    subprocess.call(command, shell=True)


def renderSmoothedGrayImage(src_path, dst_path, i):
    """
    Reads the .txt output of runOptimization() from disk, converts it to a numpy
    array, and saves it back to disk.

    Args:
        src_path: filesystem path to .txt file
        dst_path: filesystem path to which the new numpy array will be saved.
        i: some index, only used for printing/logging
    """
    print "rendering smoothed image %d ..." % i
    with open(src_path) as f:
        arr = np.asarray([int(x) for x in f.readlines()], dtype=np.uint8).reshape((HEIGHT, WIDTH))
    imsave(dst_path, arr)


########################################
#  run alpha-expansion on color image  #
########################################


def runColorOptimization(lambda1, lambda2, max_cycles):
    """
    Similar to runOptimization, but operates on a color image. It calls the
    ./smoothColor binary.
    To compile the C++ binary: `g++ gco-v3.0/smoothColor.cpp  gco-v3.0/GCoptimization.cpp gco-v3.0/graph.cpp gco-v3.0/LinkedBlockList.cpp gco-v3.0/maxflow.cpp -o smoothColor`

    This corresponds to the "Option 2: Color encoding" section in my paper.
    I couldn't get this to give good results or be fast.
    My paper does not show results from this binary.

    Args:
        lambda1: (int > 0) as defined above
        lambda2: (int > 0) as defined above
        max_cycles: (int) the max number of alpha-expansion cycles to run.

    This binary serializes the smoothed image to a .txt file defined by the src_path_pattern
    variable in main().
    """
    command = "python cat_color_image.py | ./smoothColor %i %i %i" % (lambda1, lambda2, max_cycles)
    print "command:", command
    subprocess.call(command, shell=True)


def renderSmoothedColorImage(src_path, dst_path, i):
    """
    Reads the .txt output of runColorOptimization() from disk, converts it to a
    numpy array, and saves it back to disk.

    Args:
        src_path: filesystem path to .txt file
        dst_path: filesystem path to which the new numpy array will be saved.
        i: some index, only used for printing/logging
    """
    print "rendering smoothed image %d ..." % i
    with open(src_path) as f:
        arr = np.asarray([int(x) for x in f.readlines()], dtype=np.uint8).reshape((HEIGHT, WIDTH, 3))
    imsave(dst_path, arr)


##############################
#  Grayscale Transfer logic  #
##############################


def inBounds(i, j):
    """
    Returns True iff the index (i, j) in the bounds of the image.
    """
    return 0 <= i < WIDTH and 0 <= j < HEIGHT


def computeRegion(img, (x, y)):
    """
    Given an image and pixel cooridinate, compute the region which contains that
    pixel.

    Args:
        img: 2D numpy array, represents the smoothed grayscale image
        (x, y): pixel coordinate

    Returns:
        region: the set of all (i, j) pixel coordinates in the same color-segmented
            region as (x, y).
    """
    region = set()
    color = img[y, x]

    region.add((x, y))
    stack = [(x, y)]

    while len(stack) > 0:

        x, y = stack.pop()

        neighbors = [
            (x-1, y),
            (x+1, y),
            (x, y-1),
            (x, y+1),
        ]

        for (i, j) in neighbors:
            if (i, j) in region:
                continue
            if not inBounds(i, j):
                continue
            if img[j, i] == color:
                stack.append((i, j))
                region.add((i, j))

    return region


def computeRegions(img):
    """
    Args:
        img: smoothed image. a numpy array

    Returns:
        regions: a list of regions. A region is a set of (x, y) pixel locations
            that are 4-connected and all have the same color.
    """
    seen = set()
    regions = []

    for x in range(WIDTH):
        for y in range(HEIGHT):
            if (x, y) not in seen:
                new_region = computeRegion(img, (x, y))

                assert len(seen.intersection(new_region)) == 0
                seen = seen.union(new_region)
                regions.append(new_region)

    assert len(seen) == WIDTH * HEIGHT

    return regions


def getAvgColor(img, region):
    """
    Computes the mean color for given region.

    Args:
        img: the raw color image (3D numpy array)
        region: a set of (x, y) pixel coordinates

    Returns:
        a list of length 3, where each element is the mean of its corresponding
            color channel.
    """
    return [
        sum(img[y, x, 0] for x, y in region)/len(region),
        sum(img[y, x, 1] for x, y in region)/len(region),
        sum(img[y, x, 2] for x, y in region)/len(region),
    ]


def paintRegions(img, regions):
    """
    Args:
        img: the original, unsmoothed color image (3D numpy array).
        regions: a list of regions. Each region is a set of (x, y) pixel locations
            that are 4-connected and all have the same color.

    Returns:
        painted_img: a smoothed color image (3D numpy array). The result of
            Grayscale Transfer.
    """
    # make copy of img
    painted_img = np.copy(img)

    for region in regions:
        color = getAvgColor(img, region)
        for x, y in region:
            painted_img[y, x, :] = color

    return painted_img


def show(mat):
    """
    Shows an image in a new window. Mostly for debugging purposes.

    Args:
        mat: the image to show (numpy array)
    """
    img = Image.fromarray(mat)
    img.show()


def grayscaleTransfer(gray_img, color_img):
    """
    Args:
        gray_img: smoothed grayscale image (2D numpy array)
        color_img: original, unsmoothed color image (3D numpy array)

    Returns:
        painted_img: a smoothed color image (3D numpy array). The result of
            Grayscale Transfer.
    """
    print "computing regions ..."
    regions = computeRegions(gray_img)
    print "computed %d regions" % len(regions)
    print "painting image ..."
    painted_img = paintRegions(color_img, regions)
    return painted_img


def main():
    lambda2 = 1
    max_cycles = 1
    for lambda1 in [50, 100, 200, 400, 800, 1600]:

        runOptimization(lambda1, lambda2, max_cycles)

        src_path_pattern = os.path.join(ROOT_DIR, "results/cartoon/gray/gray_%04d_%03d_%02d.txt")
        dst_path_pattern = os.path.join(ROOT_DIR, "results/cartoon/gray/gray_%04d_%03d_%02d.bmp")
        for i in range(1, max_cycles+1):
            try:
                src_path = src_path_pattern % (lambda1, lambda2, i)
                dst_path = dst_path_pattern % (lambda1, lambda2, i)
                renderSmoothedGrayImage(src_path, dst_path, i)
            except IOError:
                # the solver converged in fewer than max_cycles cycles.
                i -= 1  # back up to last successful index
                break

        # do grayscale transfer to get a smooth color image
        color_img = imread(os.path.join(ROOT_DIR, 'data/cartoon/colorFrames/colorFrame000300.jpg'))
        gray_img = imread(dst_path_pattern % (lambda1, lambda2, i))

        print "transfering to color ..."
        painted_img = grayscaleTransfer(gray_img, color_img)
        path = os.path.join(ROOT_DIR, "results/cartoon/color/transfered_%04d_%03d_%02d.bmp")
        imsave(path % (lambda1, lambda2, i), painted_img)


if __name__ == '__main__':
    main()
