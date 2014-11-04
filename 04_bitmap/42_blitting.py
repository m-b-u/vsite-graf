""" Tests the draw_bitmap, with and without masking """

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from bitmap import draw_bitmap, mask_from_bitmap

from utils import get_image_size
import numpy as np

import os, inspect

current_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

rocks_path = os.path.abspath(os.path.join(current_path, "../samples/rocks.jpg"))
alien_path = os.path.abspath(os.path.join(current_path, "../samples/Space_invader_dn.png"))

img = mpimg.imread(rocks_path)
alien = (mpimg.imread(alien_path) * 255).astype(np.uint8)

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)

dat = ax.imshow(img, interpolation='nearest', animated=True)

fb = np.empty_like(img)

x, y = 20, 0
for i in xrange(50):
    fb[:] = img[:]
    draw_bitmap(fb, x, y, alien)
    x += 4
    y += 3
    dat.set_data(fb)
    fig.canvas.draw()

mask = mask_from_bitmap(alien)

xres, yres = get_image_size(img)
x2, y2 = xres, yres
x2 = (x2 * 3) // 4
y2 = 10

img[:] = fb[:]     # keep the alien that has landed
for i in xrange(50):
    fb[:] = img[:]
    draw_bitmap(fb, x2, y2, alien, mask)
    x2 -= 3
    y2 += 2
    dat.set_data(fb)
    fig.canvas.draw()


plt.ioff()

