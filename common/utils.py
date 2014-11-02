
""" Miscelaneous utility functions for VSITE Computer Graphics


Attributes:

FIG_FORMAT (string): Set from FIG_FORMAT environment variable.
  Will be passed to savefig if set. Figures will be just saved to files,
  no interactive display

FIG_RESOLUTION (string): Set from FIG_RESOLUTION environment variable.
  Will be used to specify DPI for saving figures in case FIG_FORMAT is set.

"""

import numpy as np

import sys
import os.path
import os
import matplotlib.pyplot as plt

FIG_FORMAT = os.environ.get('FIG_FORMAT', None)
FIG_RESOLUTION = os.environ.get('FIG_RESOLUTION', None)


def get_grayscale_image(xres, yres):
    """ Creates new, zeroed array of yres rows and xres columns,
    of data type uint8 """
    return np.zeros((yres, xres), dtype=np.uint8)

def get_rgb_image(xres, yres):
    """ Creates new, zeroed array, with shape (xres, yres, 3)
    representing RGB image

    Returns: tuple with two views to array, one (xres, yres, 3)
    and other structured view, with fields 'r', 'g', 'b' for
    individual component images (used as im['r'], im['g'], im['b'])
    """
    im_rgb = np.zeros((yres, xres, 3), dtype=np.uint8)
    img = im_rgb.view(dtype=[('r', 'u1'), ('g', 'u1'), ('b', 'u1')]) [:, :, 0]
    return im_rgb, img

def get_component_view(img):
    dtype = img.dtype
    return img.view(dtype=[('r', dtype), ('g', dtype), ('b', dtype)]) [:, :, 0]

def is_rgb_image(image):
    """ Returns true if the array represents RGB image"""
    if image.ndim == 3 and image.shape[2] == 3:
        return True
    return False

def putpixel(img, x, y, value):
    """ Sets the in image array to given value

    y translates to row in matrix, x to column
    Does not check for out of bounds error, in fact masks IndexError exception

    Returns: Nothing

    """
    try:
        img[y][x] = value
    except IndexError:
        print "Coordinates: (", x, y, ") out of bounds"

def getpixel(img, x, y):
    """ Returns the value in image array on given position

    Depending on image type will be either one value or
    array of length 3 or 4 (RGB or RGBA)
    """

    return img[y][x]


def get_image_size(img):
    """ Returns the width and height of the image array """
    assert img.ndim == 2 or (img.ndim == 3 and img.shape[2] in (3, 4))
    return (img.shape[1], img.shape[0])

def plt_show():
    """ Shows the current image. Show means plt.show() if FIG_FORMAT
    is not set, or save to requested format if set.

    """

    global FIG_FORMAT
    global FIG_RESOLUTION

    if not FIG_FORMAT:
        plt.show()
        return
    prefix, _ = os.path.splitext(sys.argv[0])
    kwargs = {}
    if FIG_RESOLUTION:
        kwargs['dpi'] = int(FIG_RESOLUTION)

    kwargs['format'] = FIG_FORMAT
    name = "_%02d.%s" % (len(plt.get_fignums()), FIG_FORMAT)
    plt.savefig(prefix + name, **kwargs)
