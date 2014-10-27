from utils import get_image_size, putpixel, getpixel
import numpy as np

def draw_bitmap(img, x, y, bitmap, mask = None):
    if mask is not None:
        assert (bitmap.shape[0:2] == mask.shape)

    w, h = get_image_size(bitmap)
    for yi in xrange(h):
        for xi in xrange(w):
                m = mask is None or getpixel(mask,xi,yi)         # anything that is not 0 in mask means take that pixel
                if m:
                    putpixel(img, x+xi, y+yi, getpixel(bitmap, xi, yi))


def draw_bitmap_2(img, x, y, bitmap, mask = None):
    """ More numpy-ish way"""
    if mask is not None:
        assert (bitmap.shape[0:2] == mask.shape)

    w, h = get_image_size(bitmap)
    if mask is not None:
        if img.ndim == 3:
            img[y:y+h, x:x+w] &= ~mask[:,:,np.newaxis]        # take care of case with RGB image & single component mask
        elif img.ndim == 2:
            img[y:y+h, x:x+w] &= ~mask

    img[y:y+h, x:x+w] |= bitmap


def mask_from_bitmap(img):
    mask = np.zeros( (img.shape[0], img.shape[1]), dtype=np.uint8)
    w, h = get_image_size(img)
    for i in xrange (h):
        for j in xrange(w):
            neighbours = img[max(0,i-1) : min(i+1,h-1) ,max(0,j-1) : min(j+1, w-1)]   # in this case neighbours include pixel itself
            mask[i][j] = 255 if np.any(neighbours) else 0

    return mask
