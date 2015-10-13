""" Tests the draw_convex_polygon function
    by drawing grid of adjacent rectangles - checkerboard pattern
"""

from utils import get_grayscale_image, plt_show

from polygon import draw_convex_polygon

import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np


fig, ax = plt.subplots(1)

xres, yres = 100, 80
img = get_grayscale_image(xres, yres)


ticks = np.linspace(0, min(xres, yres)-1, endpoint=True, num=9).astype(np.int32)
x, y = np.meshgrid(ticks, ticks)
pts = np.dstack((y, x))

c = 0

for i in range(pts.shape[0]-1):
    for j in range(pts.shape[1]-1):
        draw_convex_polygon(img,
                            [pts[j][i], pts[j+1][i],
                             pts[j+1][i+1], pts[j][i+1]],
                            (((i+j) % 2) + 1) * 100)
        c += 1

ax.imshow(img, cm.gray, interpolation='nearest')

plt_show()
