import numpy as np

import sys
import os.path
import os
import matplotlib.pyplot as plt

fig_format = os.environ.get('FIG_FORMAT', None)
fig_resolution = os.environ.get('FIG_RESOLUTION', None)


def get_grayscale_image(xres, yres):
    return np.zeros( (yres, xres), dtype=np.uint8 )

def get_rgb_image(xres, yres):
    im_rgb = np.zeros((yres, xres, 3), dtype=np.uint8)
    im=im_rgb.view(dtype=[('r', 'u1'), ('g', 'u1'), ('b', 'u1')]) [:,:,0]
    return im_rgb, im

def putpixel(img, x, y, value):
    try:
        img[y][x] = value
    except:
        print "Coordinates: (", x, y, ") out of bounds"


def plt_show():
    global fig_format
    global fig_resolution

    if not fig_format:
        plt.show()
        return
    prefix, _ = os.path.splitext(sys.argv[0])
    kwargs = {}
    if fig_resolution:
        kwargs['dpi'] = int(fig_resolution)

    kwargs['format'] = fig_format
    name = "_%02d.%s" % ( len(plt.get_fignums()), fig_format)
    plt.savefig( prefix + name , **kwargs)



