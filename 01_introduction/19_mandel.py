""" Mandelbrot set example """

from utils import get_grayscale_image, get_image_size, putpixel, plt_show
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def mandel_point(c, max_iter):
    """ Iteration loop for each point, returns value, iteration number
and whether point is in Mandelbrot set"""
    z = 0
    for i in range(max_iter):
        z = z*z + c
        if abs(z) > 2.0:       # criteria for divergence
            return z, i, False
    return z, i, True

def render_mandel_iterative(img, ll_corner, ur_corner, max_iter=100):
    """ Simplest approach, iterating over every point """
    size = get_image_size(img)
    x_axis = np.linspace(ll_corner.real, ur_corner.real, num=size[0])
    y_axis = np.linspace(ur_corner.imag, ll_corner.imag, num=size[1])
    for i in range(size[1]):
        for j in range(size[0]):
            val, iteration, max_reached = mandel_point(complex(x_axis[j], y_axis[i]), max_iter)
            if not max_reached:
                putpixel(img, j, i, iteration)
            else:
                putpixel(img, j, i, 0)

default_box = [complex(-2.5, -1.5), complex(1.5, 1.5)]
box = default_box[:]

# take a look here to show image pixel per pixel
# https://stackoverflow.com/questions/8056458/display-image-with-a-zoom-1-with-matplotlib-imshow-how-to
if __name__ == '__main__':
    xres, yres = (400, 300)
    max_iter = 256
    img = get_grayscale_image(xres, yres)

    fig, ax = plt.subplots(1)
  
    def on_click(event):
        """Plot click event handler - zoom into set"""
        global box
        print(event.inaxes)
        box_width = (box[1].real - box[0].real)
        box_height = (box[1].imag - box[0].imag)
        center = complex(box[0].real + (float(event.xdata)/get_image_size(img)[0])*box_width,
                         box[0].imag + (1.0-(float(event.ydata)/get_image_size(img)[1]))*box_height)
        new_box_size = complex(box_width/1.5, box_height/1.5)
        box[0] = center - new_box_size/2
        box[1] = center + new_box_size/2

        render_mandel_iterative(img, box[0], box[1], max_iter)
        ax.imshow(img, cm.spectral, interpolation='nearest')
        plt_show()


    cid = fig.canvas.mpl_connect('button_press_event', on_click)

    render_mandel_iterative(img, box[0], box[1], max_iter)
    ax.imshow(img, cm.spectral, interpolation='nearest')
    plt_show()
    fig.canvas.mpl_disconnect(cid)
