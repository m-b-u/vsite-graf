from __future__ import division
from utils import get_grayscale_image, plt_show, putpixel
from lines import line_bresenham_int

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def standard_form_line_equation(x1, y1, x2, y2):
    """ Get the A*x + B*y + C = 0 form """
    A = y2 - y1
    B = x1 - x2
    C = - (A*x1 + B*y1) # put in any point to get C
    return A, B, C

def distance_from_line_field(img, x1, y1, x2, y2):
    A, B, C = standard_form_line_equation (x1, y1, x2, y2)
    norm = math.sqrt(A*A + B*B)
    def line_eq_eval(x, y):
        return int((A*x + B*y + C)/norm*8)      # 8 is just to scale it a bit (nicer colors)

    for i in xrange(img.shape[0]):	# rows
        for j in xrange(img.shape[1]):	# columns
            img[i][j] = line_eq_eval(j,i)       # evaluate line equation in every point


def show_line_field(im, p1, p2):
    distance_from_line_field(im, *(p1 + p2) )

    fig, ax = plt.subplots(2)
    ax[0].imshow(im, cm.rainbow_r, interpolation = 'nearest')
    ax[0].plot( *zip(p1, p2), color='w' )
    ax[0].set_xlim( 0, xres-1)
    ax[0].set_ylim( 0, yres-1)

    pixels = []
    def putpixel_collect(im, x1, y1, value):
        putpixel (im, x1, y1, value)
        pixels.append ( (x1, y1) )

    im2 = np.copy(im)

    line_bresenham_int(im2, *(p1 + p2 + ( 128, putpixel_collect)) )

    ax[1].imshow(im2, cm.rainbow_r, interpolation = 'nearest')
    ax[1].plot( *zip(p1, p2), color='b' )
    ax[1].plot( *zip(*pixels), color='b', marker='o', markersize=2, linestyle='None' )
    ax[1].set_xlim( 0, xres-1)
    ax[1].set_ylim( 0, yres-1)

    plt_show()


# Show the distance from ideal line on two examples
xres, yres = 40, 30
im = get_grayscale_image(xres, yres)

p1 = ( xres // 3, yres // 3 )
p2 = ( 2 * xres // 3, 2 * yres // 3)

show_line_field(im, p1, p2)

p1 = ( xres // 3, yres // 4 )
p2 = ( 1.3 * xres // 3, 3 * yres // 4)

show_line_field(im, p1, p2)
