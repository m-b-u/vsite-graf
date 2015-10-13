import numpy as np

import matplotlib.pyplot as plt
from utils import plt_show

def show_line_vs_pixel_grid(xres, yres):

    p1 = ( xres // 4, yres // 4)
    p2 = ( 3 * xres // 4 , 3 * yres // 4 )

    fix, axis = plt.subplots (1)
    axis.set_xlim( 0, xres-1)
    axis.set_ylim( 0, yres-1)

    axis.set_title('Line: (%s, %s) - (%s, %s)' % (p1 + p2) )

    start, end = axis.get_xlim()
    for x in np.arange(start + 0.5, end + 0.5, 1):   # draw lines at half-points manually
        axis.axvline (x, color='lightgray')

    axis.xaxis.set_ticks(xran+ge(int(start), int(end+1)))

    start, end = axis.get_ylim()
    for y in np.arange(start + 0.5, end + 0.5, 1):
        axis.axhline (y, color='lightgray')

    axis.yaxis.set_ticks(xrange(int(start), int(end+1)))

    axis.plot( *zip(p1, p2), color='g' )
    axis.plot( *zip(p1, p2), color='b', marker='o', markersize=3, linestyle='None' )

    plt_show()



# show the 'ideal' line vs pixel grid
xres, yres = 24, 18
show_line_vs_pixel_grid(xres, yres)
