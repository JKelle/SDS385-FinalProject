
import numpy as np
import pylab
import imageio
import scipy.misc
import os



def f(i, j):
    prev_frame = vid.get_data(i)
    cur_frame = vid.get_data(j)
    diffs = abs(cur_frame - prev_frame).sum(axis=2)
    diffs = diffs.reshape(360*640)
    diffs = diffs[diffs > 0]
    return sorted(diffs)


def main():
    filename = 'S01E25_MirrorGem.mp4'
    vid = imageio.get_reader(filename, 'ffmpeg')

    # for i, img in enumerate(vid):
    #     if i == 0:
    #         prev_img = img
    #         continue

    frame_delta = 2
    threshold = 20
    prev_frame = None
    result_frame = np.zeros([360, 640, 3], dtype=np.uint8)

    for i in range(0, vid.get_length(), frame_delta):
        print "computing frame #%d" % i

        if i == 0:
            prev_frame = vid.get_data(i)
            continue

        cur_frame = vid.get_data(i)
        diff = abs(cur_frame - prev_frame).sum(axis=2)
        diff[diff < threshold] = 0

        result_frame.fill(255)
        for y, x in zip(*diff.nonzero()):
            result_frame[y, x, :] = cur_frame[y, x, :]

        output_path = os.path.join("resultFrames/delta%d" % frame_delta, "frame%05d.jpg" % i)
        scipy.misc.toimage(result_frame, cmin=0.0, cmax=255).save(output_path)

        prev_frame = cur_frame

    # for img, label in ((img1, "img1"), (img2, "img2"), (diff, "diff"), (result_frame, "result_frame")):
    #     fig = pylab.figure()
    #     fig.suptitle(label, fontsize=20)
    #     pylab.imshow(img, cmap='bwr')
    # pylab.show()


if __name__ == '__main__':
    main()
