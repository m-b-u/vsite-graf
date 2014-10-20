from __future__ import division

from utils import get_grayscale_image, putpixel, plt_show
import numpy as np


import matplotlib.pyplot as plt
import matplotlib.cm as cm

def line_dda(img, x1, y1, x2, y2, value, putpixel=putpixel):
    m = (y2 - y1) / (x2 - x1)
    error = []
    if abs(m) <= 1:
        dy = m
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        y = y1
        for x in xrange(x1, x2 + 1):
            putpixel(img, x, int(round(y)), value)
            error.append ( (x, y-round(y)) )
            y += dy
    else:
        dx = 1/m
        if y1 > y2:
            y1, y2 = y2, y1
            x1, x2 = x2, x1
        x = x1
        for y in xrange(y1, y2 + 1):
            putpixel(img, int(round(x)), y, value)
            error.append ( (y, x-round(x)) )
            x += dx
    return error

def standard_form_line_equation(x1, y1, x2, y2):
    """ Get the A*x + B*y + C = 0 form """
    A = y2 - y1
    B = x1 - x2
    C = - (A*x1 + B*y1) # put in any point to get C
    return A, B, C

def distance_from_line_field(img, x1, y1, x2, y2):
    A, B, C = standard_form_line_equation (x1, y1, x2, y2)
    norm = math.sqrt(A*A + B*B)
    def line_eq_eval(x, y):
        return int((A*x + B*y + C)/norm*8)      # 8 is just to scale it a bit (nicer colors)

    for i in xrange(img.shape[0]):	# rows
        for j in xrange(img.shape[1]):	# columns
            img[i][j] = line_eq_eval(j,i)       # evaluate line equation in every point


def line_bresenham_int (img, x1, y1, x2, y2, value, putpixel=putpixel):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    putpixel (img, x1, y1, value)
    if dy <= dx: 
        # Line slope is closer to x axis 
        if x2 < x1:
            y1, y2 = y2, y1
            x1, x2 = x2, x1
        yy = 1 if y1 <= y2 else -1 # direction in which we increment x axis
        y = y1
        D = 2*dy - dx
        for x in xrange(x1 + 1, x2 + 1):
            if D > 0:
                y += yy
                D += (2*dy - 2*dx)
            else:
                D += 2*dy
            putpixel(img, x, y, value)
    else:     
        # Line slope is closer to y axis
        if y2 < y1:
            y1, y2 = y2, y1
            x1, x2 = x2, x1
        xx = 1 if x1 <= x2 else -1 # direction in which we increment x axis
        x = x1
        D = 2*dx - dy
        putpixel (img, x1, y1, value)
        for y in xrange(y1 + 1, y2 + 1):
            if D > 0: 
                x += xx
                D += (2*dx - 2*dy)
            else:
                D += 2*dx
            putpixel(img, x, y, value)

def show_line_field(im, p1, p2):
    distance_from_line_field(im, *(p1 + p2) )

    fig, ax = plt.subplots(2)
    ax[0].imshow(im, cm.rainbow_r, interpolation = 'nearest')
    ax[0].plot( *zip(p1, p2), color='w' )
    ax[0].set_xlim( 0, xres-1) 
    ax[0].set_ylim( 0, yres-1) 

    pixels = []
    def putpixel_collect(im, x1, y1, value):
        putpixel (im, x1, y1, value)
        pixels.append ( (x1, y1) )

    im2 = np.copy(im)

    line_bresenham_int(im2, *(p1 + p2 + ( 128, putpixel_collect)) )

    ax[1].imshow(im2, cm.rainbow_r, interpolation = 'nearest')
    ax[1].plot( *zip(p1, p2), color='b' )
    ax[1].plot( *zip(*pixels), color='b', marker='o', markersize=2, linestyle='None' )
    ax[1].set_xlim( 0, xres-1) 
    ax[1].set_ylim( 0, yres-1) 

    plt_show()


def show_line_test(xres, yres, line_func):
    im = get_grayscale_image(xres, yres)

    center = (xres // 2, yres // 2)
    a, b = 15, 10
    

    def test_line(center, segments, line_func):
        angle_step = 2*math.pi/segments
        for i in xrange(segments):
            angle = i * angle_step    # angle in radians
            line_func (im, center[0], center[1], 
                       center[0] + int(a*math.cos(angle)),
                       center[1] + int(b*math.sin(angle)),
                       int(256.0*(i+1)/segments)-1)

    #test_line(center, 12, line_dda)
    test_line(center, 12, line_bresenham_int)

    line = line_bresenham_int
    line(im, 0, 0, xres-1, 0, 255)
    line(im, xres-1, 0, xres-1, yres-1, 255)
    line(im, xres-1, yres-1, 0, yres-1, 255)
    line(im, 0, yres-1, 0, 0, 255)

    plt.subplots(1)[1].imshow(im, cm.gray, interpolation = 'nearest')

    plt_show()

def show_line_dda_with_rounding_error(xres, yres):
    im = get_grayscale_image(xres, yres)

    p1 = ( xres // 3, yres // 3 )
    p2 = ( 2 * xres // 3, 2 * yres // 3)

    dx = abs(p1[0]-p2[0])
    dy = abs(p1[1]-p2[1])

    args = {}
    if dx > dy:
        args['sharex'] = True
    else:
        args['sharey'] = True

    error = line_dda(im, *(p1 + p2 + ( 255, )) )
    fig, axis = plt.subplots( 2, **args )
    
    axis[0].imshow(im, cm.gray, interpolation = 'nearest')
    axis[0].plot( *zip(p1, p2), color='g' )
    axis[0].set_xlim( 0, xres-1) 
    axis[0].set_ylim( 0, yres-1) 

    axis[1].plot(*zip(*error))
    #axis[1].set_aspect(1)
    #axis[1].set_autoscaley_on(False)
    #axis[1].set_ylim( -0.6, 0.6 )

    plt_show()

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

    axis.xaxis.set_ticks(xrange(int(start), int(end+1)))

    start, end = axis.get_ylim()
    for y in np.arange(start + 0.5, end + 0.5, 1):
        axis.axhline (y, color='lightgray')

    axis.yaxis.set_ticks(xrange(int(start), int(end+1)))



    #axis.grid(True, linestyle='-')
    
    #po1 = ( p1[0] + 0.5, p1[1] + 0.5)
    #po2 = ( p2[0] + 0.5, p2[1] + 0.5)

    axis.plot( *zip(p1, p2), color='g' )
    axis.plot( *zip(p1, p2), color='b', marker='o', markersize=3, linestyle='None' )


    plt_show()

if __name__=='__main__':
    import math

    # show the 'ideal' line vs pixel grid
    xres, yres = 24, 18
    show_line_vs_pixel_grid(xres, yres)

    # reset the image
    xres, yres = 120, 60

    show_line_dda_with_rounding_error(xres, yres)
    
    # Show the distance from ideal line on two examples
    xres, yres = 40, 30
    im = get_grayscale_image(xres, yres)

    p1 = ( xres // 3, yres // 3 )
    p2 = ( 2 * xres // 3, 2 * yres // 3)

    show_line_field(im, p1, p2)

    p1 = ( xres // 3, yres // 4 )
    p2 = ( 1.3 * xres // 3, 3 * yres // 4)

    show_line_field(im, p1, p2)

    # Test the line with points on ellipse
    xres, yres = 40, 30
    show_line_test(xres, yres, line_dda)
