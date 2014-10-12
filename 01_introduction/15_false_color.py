import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import sys

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])


if __name__=='__main__':
    if len(sys.argv) < 2:
        print "usage: " + sys.argv[0] + " image_filename [colormap_name]"
        sys.exit(1)
    img = None
    try:
        img = mpimg.imread(sys.argv[1])
    except:
        print "Error loading image: " + sys.argv[1]
        sys.exit(-1)

    gray = rgb2gray(img)

    fix, axis = plt.subplots(2, sharex = True)

    axis[0].imshow(gray, cmap = plt.get_cmap('gray'), aspect = 1)
    axis[0].set_title('Grayscale')

    cmap_name = 'gist_rainbow' if len(sys.argv) <= 2 else sys.argv[2]
    print "Using: %s as color map." % cmap_name
    cmap = plt.get_cmap(cmap_name)
    try:
        cmap = plt.get_cmap(cmap_name)
    except ValueError:
        print "Color map not found, exiting"
        sys.exit(1)

    axis[1].imshow(gray, cmap = cmap, aspect = 1)
    axis[1].set_title(cmap_name)
    plt.show()
