
from utils import putpixel

def line_dda(img, x1, y1, x2, y2, value, putpixel=putpixel):
    m = 0
    one_over_m = 0
    try:
        m = (y2 - y1) / (x2 - x1)
        one_over_m = 1/m
    except ZeroDivisionError:
        m = 1e9 # some large number, won't really be used. One over m will stay 0
    error = []
    if abs(m) <= 1:
        dy = m
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        y = y1
        for x in range(x1, x2 + 1):
            putpixel(img, x, int(round(y)), value)
            error.append ( (x, y-round(y)) )
            y += dy
    else:
        dx = one_over_m
        if y1 > y2:
            y1, y2 = y2, y1
            x1, x2 = x2, x1
        x = x1
        for y in range(y1, y2 + 1):
            putpixel(img, int(round(x)), y, value)
            error.append ( (y, x-round(x)) )
            x += dx
    return error


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
        for x in range(x1 + 1, x2 + 1):
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
        for y in range(y1 + 1, y2 + 1):
            if D > 0: 
                x += xx
                D += (2*dx - 2*dy)
            else:
                D += 2*dx
            putpixel(img, x, y, value)


