""" Functions to draw bitmap over another bitmap.
    Also derive 1-neighbourhood mask for given bitmap
"""


from utils import get_image_size, putpixel, getpixel
import numpy as np

def draw_bitmap(img, x, y, bitmap, mask=None):
    """ Draws bitmap on image array, on positions x, y
    optionally using mask
    """
    if mask is not None:
        assert bitmap.shape[0:2] == mask.shape

    w, h = get_image_size(bitmap)
    for yi in xrange(h):
        for xi in xrange(w):
            # anything that is not 0 in mask means take that pixel
            m = mask is None or getpixel(mask, xi, yi)
            if m:
                putpixel(img, x+xi, y+yi, getpixel(bitmap, xi, yi))


def draw_bitmap_2(img, x, y, bitmap, mask=None):
    """ More numpy-ish way"""
    if mask is not None:
        assert bitmap.shape[0:2] == mask.shape

    w, h = get_image_size(bitmap)
    if mask is not None:
        if img.ndim == 3:
            # take care of case with RGB image & single component mask
            img[y:y+h, x:x+w] &= ~mask[:, :, np.newaxis]
        elif img.ndim == 2:
            img[y:y+h, x:x+w] &= ~mask
        img[y:y+h, x:x+w] |= bitmap
    else:
        img[y:y+h, x:x+w] = bitmap
        # Try: To see "unexpected" effects of bitwise logical operations
        # on 8-bit RGB images - comment out the line above, and comment one below
        # img[y:y+h, x:x+w] |= bitmap

def mask_from_bitmap(img):
    """ Derive mask for blitting image img. Mask has value 255
    iff given pixel or any in its neighbourhood has
    nonzero value, 0 otherwise"""

    mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    w, h = get_image_size(img)
    for i in xrange(h):
        for j in xrange(w):
            # in this case neighbours include pixel itself
            neighbours = img[max(0, i-1) : min(i+1, h-1),
                             max(0, j-1) : min(j+1, w-1)]
            mask[i][j] = 255 if np.any(neighbours) else 0

    return mask
