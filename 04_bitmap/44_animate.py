""" Do some animation, multiple blits, test draw_bitmap_2 """

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from bitmap import draw_bitmap_2, mask_from_bitmap

from utils import get_image_size
import numpy as np

img = mpimg.imread("../samples/rocks_red.jpg")

xres, yres = get_image_size(img)

alien = (mpimg.imread("../samples/Space_invader_dn_c.png") * 255) \
    .astype(np.uint8)
mask = mask_from_bitmap(alien)
alien2 = (mpimg.imread("../samples/Space_invader_up_c.png") * 255) \
    .astype(np.uint8)
mask2 = mask_from_bitmap(alien2)


alien = [alien, alien2]
mask = [mask, mask2]
# comment out to test animation without masks
# mask = [None, None]


def draw_fleet(fb, x, y, rows, columns, padding, alien, mask, img_idx):
    """ Draw table with same bitmap"""
    w, h = get_image_size(alien[img_idx])
    for i in range(columns):
        for j in range(rows):
            draw_bitmap_2(fb, x + i*(w+padding), y + j*(h+padding),
                          alien[img_idx], mask[img_idx])

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)

dat = ax.imshow(img, interpolation='nearest', animated=True)

fb = np.empty_like(img)



def animate():
    """ Draw alien fleet repeatedly, taking care
    of descending to next row when appropriate"""
    global fig


    w, h = get_image_size(alien[0])
    rows = 4
    columns = 10
    padding = 10

    yend = yres - rows * (h + padding)
    # last column does not need right padding
    row_width = (w + padding) * columns - padding


    y = 0
    x = padding
    xdelta = 3
    ydelta = 4
    flip_freq = 10
    frame_num = 0
    img_idx = 0
    key = False
    def on_key_press(event):
        print("Key!")
        key = True
    #hid = fig.canvas.mpl_connect('key_press_event', on_key_press)
    while y <= yend and not key:
        frame_num += 1
        fb[:] = img[:]
        x += xdelta

        if frame_num % flip_freq == 0:
            img_idx += 1
            if img_idx >= len(alien):
                img_idx = 0

        if x + row_width >= xres:
            x -= (x + row_width) % xres
            xdelta = -xdelta
            y += ydelta
        elif x < 0:
            xdelta = -xdelta
            x = x + xdelta
            y += ydelta
        draw_fleet(fb, x, y, rows, columns, padding, alien, mask, img_idx)

        dat.set_data(fb)
        fig.canvas.draw()
        plt.pause(0.001)

    #fig.canvas.mpl_disconnect(hid)

animate()

plt.ioff()
#plt_show()
