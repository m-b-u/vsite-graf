from utils import get_grayscale_image, putpixel, plt_show

from polygon import draw_convex_polygon, plot_polygon

import matplotlib.pyplot as plt
import matplotlib.cm as cm

fig, ax = plt.subplots(1)

xres, yres = 320, 240
img = get_grayscale_image(xres, yres)

point = [ (0. ,0.), (1., 0.), (1., 1.) ]

import math

scale = 30
center = xres/2, yres/2
for i in xrange(2):

    pts = [ (int (center[0] + p[0]*scale), int(center[1] + p[1]*scale) ) for p in point]
    try:
        draw_convex_polygon(img, pts, 50+ i*10) # [200, 100, 50]
    except Exception as e:
        print e.message
    plot_polygon (ax, pts, 'w')
    x, y = point[2]
    norm = math.sqrt(x*x + y*y)
    new_point = (x + -y/norm, y + x/norm)      # orthogonal to x,y ,
    point[1] = point[2]
    point[2] = new_point

ax.imshow(img, cm.gray, interpolation = 'nearest')

plt_show()
