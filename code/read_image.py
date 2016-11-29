
import numpy as np
from scipy.misc import imsave


WIDTH = 640
HEIGHT = 360
NUM_LABELS = 256


for i in range(1, 10):
    print "reading output file", i, "..."
    with open("output%i.res" % i) as f:
        arr = np.asarray([int(x) for x in f.readlines()], dtype=np.uint8).reshape((HEIGHT, WIDTH))
    imsave("output%i.bmp" % i, arr)
