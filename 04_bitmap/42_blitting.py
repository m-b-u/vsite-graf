import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from bitmap import draw_bitmap, mask_from_bitmap

from utils import get_grayscale_image, plt_show, get_image_size
import numpy as np
import random

img = mpimg.imread("../samples/rocks_red.jpg")
alien = (mpimg.imread("../samples/Space_invader_dn_c.png") * 255).astype(np.uint8)

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)

#dat = ax.imshow(ui,cmap=cm.jet)
dat = ax.imshow(img, interpolation='nearest', animated = True)

fb = np.empty_like(img)

x, y = 20 , 0
for i in xrange (50):
    fb[:] = img[:]
    draw_bitmap (fb, x, y, alien)
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
for i in xrange (50):
    fb[:] = img[:]
    draw_bitmap (fb, x2, y2, alien, mask)
    x2 -= 3
    y2 += 2
    dat.set_data(fb)
    fig.canvas.draw()

w, h = get_image_size(alien)
rows = 4
columns = 10
padding = 10

yend = yres - rows * (h + padding) 
row_width = (w + padding) * columns - padding # last column does not need right padding

from bitmap import draw_bitmap_2
def draw_fleet(fb, x, y, padding, alien, mask, img_idx):
    w, h = get_image_size(alien[img_idx])

    for i in xrange(columns):
        for j in xrange(rows):
            draw_bitmap_2 (fb, x + i*(w+padding), y + j*(h+padding), alien[img_idx], mask[img_idx])

# reread the background
img = mpimg.imread("../samples/rocks_red.jpg")
# read another alien image

alien2 = (mpimg.imread("../samples/Space_invader_up_c.png") * 255).astype(np.uint8)
mask2 = mask_from_bitmap(alien2)

alien = [alien, alien2]
mask = [mask, mask2]



def animate():
    global fig

    y = 0
    x = padding
    xdelta = 3
    ydelta = 4
    flip_freq = 10
    frame_num = 0
    img_idx = 0
    key = False
    def on_key_press(event):
        print "Key!"
        key = True
    
    hid = fig.canvas.mpl_connect('key_press_event', on_key_press)
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
        draw_fleet(fb, x, y, padding, alien, mask, img_idx)

        dat.set_data(fb)
        fig.canvas.draw()

    fig.canvas.mpl_disconnect(hid)

animate()

plt.ioff()
#plt_show()
