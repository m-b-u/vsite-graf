import matplotlib.pyplot as plt
import matplotlib.cm as cm
from utils import plt_show, get_grayscale_image
from lines import line_bresenham_int, line_dda

import math

def show_line_test(xres, yres, line_func):
    im = get_grayscale_image(xres, yres)

    center = (xres // 2, yres // 2)
    a, b = 15, 10

    def test_line(center, segments, line_func):
        x0 = center[0] + int(a*math.cos(0))
        y0 = center[1] + int(b*math.sin(0))

        angle_step = 2*math.pi/segments
        for i in range(1, segments+1):

            angle = i * angle_step    # angle in radians
            x = center[0] + int(a*math.cos(angle))
            y  = center[1] + int(b*math.sin(angle))
            line_func (im, x0, y0, x, y, 
                       int(256.0*(i+1)/segments)-1)
            x0 = x
            y0 = y

    test_line(center, 12, line_func)

    line_func(im, 0, 0, xres-1, 0, 255)
    line_func(im, xres-1, 0, xres-1, yres-1, 255)
    line_func(im, xres-1, yres-1, 0, yres-1, 255)
    line_func(im, 0, yres-1, 0, 0, 255)

    plt.subplots(1)[1].imshow(im, cm.gray, interpolation = 'nearest')

    plt_show()


# Test the line with points on ellipse
xres, yres = 40, 30
show_line_test(xres, yres, line_dda)
# test Bresenham, because I just notices some errors in dda :-)
# no top and bottom horizontal line
