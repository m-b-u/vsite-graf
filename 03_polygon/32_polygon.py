from utils import get_grayscale_image, putpixel, plt_show

from polygon import draw_convex_polygon, plot_polygon

import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np



fig, ax = plt.subplots(1)

xres, yres = 160, 120
img = get_grayscale_image(xres, yres)

poly1 = [ (0, 0), (100, 0), (100, 50), (75, 75), (50, 50), (25,75), (0, 50) ]

poly2 = [ (0, 50), (25, 75), (50, 50), (75, 75), (100, 50), (100, 100), (0, 100)]
plot_polygon(ax, poly1, 'y')
plot_polygon(ax, poly2, 'w')
draw_convex_polygon(img, poly1, 200)
draw_convex_polygon(img, poly2, 100)

#poly = [ (0, 0), (1, 0), (1, 1), (-0.5, 2), (-1.2, 1.5) ]
#
#
#for i in xrange(1):
#    p = np.array(poly, dtype=np.float32)
#    p *= (i+1) * 20
#    p += min(xres, yres)//2
#    print "Poly: ", p
#    draw_convex_polygon(img, p.astype(np.int32), 255)



## issues. Either first or last scanline should have exactly one pixel
poly3 =  [ (42, 42), (32, 52), (42, 62) , (52, 52) ]
draw_convex_polygon(img, poly3, 255)
plot_polygon(ax, poly3, 'r')

## issue, considering only right edge:
#Y: 11 considering edges: [(20, 30, ((30, 10), (30, 20)))]
#Intersections at y:  [30]
poly4 = [ (10, 10), (30, 10), (30, 20) , (20, 20) ]
draw_convex_polygon(img, poly4, 255)
plot_polygon(ax, poly4, 'g')

ax.imshow(img, cm.gray, interpolation = 'nearest')

plt_show()
