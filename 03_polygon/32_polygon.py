from utils import get_grayscale_image, putpixel, plt_show

from polygon import draw_convex_polygon

import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np



fig, ax = plt.subplots(1)

xres, yres = 100, 80
img = get_grayscale_image(xres, yres)


#poly = [ (0, 0), (1, 0), (1, 1), (-0.5, 2), (-1.2, 1.5) ]
#
#
#for i in xrange(1):
#    p = np.array(poly, dtype=np.float32)
#    p *= (i+1) * 20
#    p += min(xres, yres)//2
#    print "Poly: ", p
#    draw_convex_polygon(img, p.astype(np.int32), 255)





ticks = np.linspace (0, min(xres,yres) -1, endpoint=True, num = 9).astype(np.int32)
x, y = np.meshgrid(ticks, ticks)
pts = np.dstack ( (y, x) )

c = 0

for i in xrange(pts.shape[0]-1 ):
    for j in xrange(pts.shape[1]-1):
        draw_convex_polygon( img, [ pts[j][i], pts[j+1][i], pts[j+1][i+1], pts[j][i+1]] , (((i+j) % 2) + 1 ) * 100)
        c += 1


## issues. Either first or last scanline should have exactly one pixel
draw_convex_polygon(img, [ (40, 40), (30, 50), (40, 60) , (50, 50) ], 255)

## issue, considering only right edge:
#Y: 11 considering edges: [(20, 30, ((30, 10), (30, 20)))]
#Intersections at y:  [30]
draw_convex_polygon(img, [ (10, 10), (30, 10), (30, 20) , (10, 20) ], 255)


ax.imshow(img, cm.gray, interpolation = 'nearest')

plt_show()
