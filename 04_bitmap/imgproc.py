""" Module with basic image processing functions"""

import numpy as np
from utils import is_rgb_image, get_component_view

def convert_from_uint8(img):
    """Convert image in uint8 [0..255] to [0.0..1.0] float32"""
    return img.astype(np.float32) / 255.0

def convert_to_uint8(img):
    """Convert image in [0.0..1.0] float32 to uint8 [0..255]"""
    return (img * 255).astype(np.uint8)

def get_image_minmax (img):
    """Get minimum and maximum value of any pixel component in the image"""
    print "Image min, max: ", img.min(), img.max()
    return img.min(), img.max()

def adjust_levels(img, in_levels, out_levels, gamma=1.0):
    """ Perform level adjustments and gamma correction
    Args: img - image to be adjusted
          in_levels - (input_low, input_high) tuple,
                      image will be taken as if these
                      were the input limits, regardless of real values
          out_levels - (output_low, output_high),
                       these will be limits for output image
          gamma - taken to be the gamma of the input image
    Returns: adjusted image (copy)
    """
    buf = img.copy()
    dtype = img.dtype
    if dtype == np.uint8:
        in_levels = (in_levels[0]/255.0, in_levels[1]/255.0)
        out_levels = (out_levels[0]/255.0, out_levels[1]/255.0)
        buf = convert_from_uint8(img)
    get_image_minmax(buf)
    buf = (buf - in_levels[0]) / (in_levels[1] - in_levels[0])
    np.clip(buf, 0., 1., out=buf)
    buf = np.power (buf ,1/gamma)
    # if gamma is not 1 input image should be converted to [0-1] float values

    get_image_minmax(buf)
    buf *= (out_levels[1]-out_levels[0])
    get_image_minmax(buf)
    buf += out_levels[0]
    get_image_minmax(buf)

    np.clip(buf, 0., 1., out=buf)
    get_image_minmax(buf)

    if dtype == np.uint8:
        return convert_to_uint8(buf)
    else:
        return buf

def auto_levels(img):
    """ Determine the absolute minimum and maximum of the input image 
    and call adjust_levels to stretch it to [0..1] or [0..255] 
    depending on type of input image"""

    out_levels = (0, 255) if img.dtype == np.uint8 else (0.0, 1.0)
    return adjust_levels(img, get_image_minmax(img), out_levels)

def apply_with_amount(img, filter_func, amount):
    """ Call the 'filter_func' without arguments on the image and return 
    linear combination of filtered and original image"""
    return img * (1. - amount) + filter_func(img) * amount

#def apply_kernel(image, kernel):
 #   img = image.copy()
 #   if is_rgb_image(img):
 #       im = get_component_view(img)
 #       im['r'] = np.convolve(im['r'], kernel)
 #       im['g'] = np.convolve(im['g'], kernel)
 #       im['b'] = np.convolve(im['b'], kernel)
 #       return im
 #   else:
 #       return np.convolve(image, kernel)


import scipy.signal
#import scipy.ndimage
# Faster alternative would be: Horizontal and vertical pass with 1D convolution
# How to split kernel automaticaly?

def normalize_kernel(kernel):
    """ Normalize the convolution kernel so that sum of all
    element equals 1"""
    sum_ = np.sum(kernel)
    if abs(sum_) > 1e-10:
        return kernel / sum_

def apply_kernel(image, kernel, clip=True):
    """Apply the 2D convolution kernel to image"""
    img = image.copy()

    def conv(mat):
        """ Apply the kernel to 2D matrix"""
        buf = scipy.signal.convolve2d(mat, kernel)
        if clip:
            np.clip(buf, 0., 1., out=buf)
        return buf

    if is_rgb_image(img):
        im = get_component_view(img)
        return np.dstack([conv(im['r']), conv(im['g']), conv(im['b'])])
    else:
        return conv(img)

def blur_uniform(img):
    """ Kernel op: 3x3 box blur"""
    kernel = np.ones((3, 3))
    kernel /= float(kernel.size)
    return apply_kernel(img, kernel)

def blur_gaussian(img):
    """ Kernel op: 3x3 Gaussian blur"""
    kernel = np.array([[1., 2., 1.],
                      [2., 4., 2.],
                      [1., 2., 1.]], dtype=np.float32)
    kernel = normalize_kernel(kernel)
    return apply_kernel(img, kernel)

def sharpen(img):
    """ Kernel op: 3x3 Cross sharpen"""
    kernel = np.array([[0., -1., 0.], 
                      [-1., 5., -1.],
                      [0., -1., 0.]], dtype=np.float32)

# alternative kernel
#    kernel = np.array([[-1., -1., -1.], 
#                      [-1., 9., -1.],
#                      [-1., -1., -1.]], dtype=np.float32)

    kernel = normalize_kernel(kernel) 
    return apply_kernel(img, kernel)

def unsharp(img):
    """ Kernel op: 5x5 unsharp (without mask)"""
    kernel = np.array([[1., 4., 6., 4., 1.],
                      [4., 16., 24., 16., 4.],
                      [6., 24., -476., 24., 6],
                      [4., 16., 24., 16., 4.],
                      [1., 4., 6., 4., 1.]], dtype=np.float32)
    kernel = normalize_kernel(kernel) 
    return apply_kernel(img, kernel)

def edge_hv(img):
    """ Horizontal and vertical edge detection """
    kernel = np.array([[-1., -1., -1.],
                      [-1., 8., -1.],
                      [-1., -1., -1.]], dtype=np.float32)
    # this kernel is not normalized: sum is zero
    return apply_kernel(img, kernel)
