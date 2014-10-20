from __future__ import division

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.cm as cm

from utils import get_grayscale_image, putpixel, plt_show
from lines import line_bresenham_int, line_dda

def show_line_dda_with_rounding_error(xres, yres):
    im = get_grayscale_image(xres, yres)

    p1 = ( xres // 5, yres // 3 )
    p2 = ( 4 * xres // 5, 2 * yres // 3)

    dx = abs(p1[0]-p2[0])
    dy = abs(p1[1]-p2[1])

    args = {}
    if dx > dy:
        args['sharex'] = True
    else:
        args['sharey'] = True

    error = line_dda(im, *(p1 + p2 + ( 255, )) )
    fig, axis = plt.subplots( 2, **args )
    
    axis[0].imshow(im, cm.gray, interpolation = 'nearest')
    axis[0].plot( *zip(p1, p2), color='g' )
    axis[0].set_xlim( 0, xres-1) 
    axis[0].set_ylim( 0, yres-1) 

    axis[1].plot(*zip(*error))
    #axis[1].set_aspect(1)
    #axis[1].set_autoscaley_on(False)
    #axis[1].set_ylim( -0.6, 0.6 )

    plt_show()


# reset the image
xres, yres = 120, 30

show_line_dda_with_rounding_error(xres, yres)

