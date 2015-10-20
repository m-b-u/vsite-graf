""" Mandelbrot set example """

from utils import get_grayscale_image, get_image_size, putpixel, plt_show
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm




""" Iteration loop for each point, returns value, iteration number
and whether point is in Mandelbrot set"""
def mandel_point(c, max_iter):
    z = 0
    for i in xrange(max_iter):
        z = z*z + c
        if abs(z) > 2.0:       # criteria for divergence
            return z, i, False
    return z, i, True

""" Simplest approach, iterating over every point """
def render_mandel_iterative(img, ll_corner, ur_corner, max_iter = 100):
    size = get_image_size(img)
    x_axis = np.linspace(ll_corner.real, ur_corner.real, num=size[0])
    y_axis = np.linspace(ur_corner.imag, ll_corner.imag, num=size[1])
    for i in xrange(size[1]):
        for j in xrange(size[0]):
            val, iter, max_reached = mandel_point(complex(x_axis[j],y_axis[i]), max_iter)
            if not max_reached:
                putpixel(img, j, i, iter)

        print 

if __name__=='__main__':
  xres, yres = (300, 200)
  img = get_grayscale_image(xres, yres)

  ll_corner = complex(-2.5, -1.5)
  ur_corner = complex(1.5, 1.5)
  max_iter = 60
  
  render_mandel_iterative(img, ll_corner, ur_corner, max_iter)

  fig, ax = plt.subplots(1)
  ax.imshow(img, cm.spectral, interpolation='nearest')
  plt_show()
