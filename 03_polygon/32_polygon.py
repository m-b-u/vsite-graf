"""
   Tests the draw_polygon with some simple shapes
"""

from utils import get_grayscale_image, plt_show

from polygon import draw_polygon, plot_polygon

import matplotlib.pyplot as plt
import matplotlib.cm as cm


fig, ax = plt.subplots(1)

xres, yres = 160, 120
img = get_grayscale_image(xres, yres)

poly1 = [(0, 0), (100, 0), (100, 50), (75, 75), (50, 50), (25, 75), (0, 50)]

poly2 = [(0, 50), (25, 75), (50, 50), (75, 75), (100, 50), (100, 100), (0, 100)]
plot_polygon(ax, poly1, 'y')
plot_polygon(ax, poly2, 'w')
draw_polygon(img, poly1, 200)
draw_polygon(img, poly2, 100)


## issues. Either first or last scanline should have exactly one pixel
poly3 = [(42, 22), (32, 32), (42, 42), (52, 32)]
draw_polygon(img, poly3, 255)
plot_polygon(ax, poly3, 'r')


poly4 = [(10, 10), (30, 10), (30, 20), (20, 20), (12, 18)]
draw_polygon(img, poly4, 255)
plot_polygon(ax, poly4, 'g')

ax.imshow(img, cm.gray, interpolation='nearest')

plt_show()
