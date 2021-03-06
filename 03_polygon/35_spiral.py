""" Test draw_convex_polygon with some triangles,
    sharing one vertex and one edge (Spiral of Theodorus,
    square root spiral, Einstein spiral, Pythagorean spiral"""

from utils import get_rgb_image, plt_show

from polygon import draw_polygon, plot_polygon

import matplotlib.pyplot as plt
import matplotlib.cm as cm

fig, ax = plt.subplots(1)

xres, yres = 320, 240
img, img_ = get_rgb_image(xres, yres)

point = [(0., 0.), (-1., 0.), (-1., -1.)]

import math

scale = 30
center = xres/2, yres/2
for i in xrange(15):

    pts = [(int(center[0] + p[0]*scale),
            int(center[1] + p[1]*scale)) for p in point]

    draw_polygon(img, pts, [i*10, 20+i*15, 50 + i*10])

    plot_polygon(ax, pts, 'w')
    x, y = point[2]
    norm = math.sqrt(x*x + y*y)
    new_point = (x + -y/norm, y + x/norm)      # orthogonal to x,y ,
    point[1] = point[2]
    point[2] = new_point

ax.imshow(img, cm.gray, interpolation='nearest')

plt_show()
