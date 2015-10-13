

from utils import get_rgb_image, putpixel
import math

def filled_circle_slow(img, center, radius, value):
  """
  Go over every pixel, and check its distance to center
  """

  r2 = radius * radius
  for i in range(img.shape[0]):    # rows
    for j in range(img.shape[1]):  # columns
      if (center[0] - j) * (center[0] - j) + (center[1] - i) * (center[1] - i) <= r2:
        img[i][j] = value
  pass

def filled_circle_scanline(img, center, radius, value):
  r2 = radius * radius
  for i in range(center[1] - radius, center[1] + radius):
    width = int(math.sqrt (r2 - (center[1] - i) * (center[1] - i)))
    img[i][(center[0] - width):(center[0] + width)] = value

def filled_circle_vectorized(img, center, radius):
  # np.where
  """
  https://www.wakari.io/sharing/bundle/travis/CircleMask
  def circ(h, k, r, x, y):
    return (x-h)**2 + (y-k)**2 <= r**2

  x, y = np.indices(myim.shape)
  imshow(circ(180, 200, 120, x, y))
  """
  pass


if __name__=='__main__':
  xres, yres = (300, 200)
  _im, im = get_rgb_image(xres, yres)

  circle = filled_circle_scanline
  #circle = circle_and_blank_vectorized

  circle (im['r'], (int(xres/3), int(yres/3)), int(yres/3), 255)
  circle (im['g'], (int(2*xres/3), int(yres/3)), int(yres/3), 255)
  circle (im['b'], (int(xres/2), int(2*yres/3)), int(yres/3), 255)

  import matplotlib.pyplot as plt
  plot = plt.figure(1).add_subplot (111)
  plot.imshow(_im)
  plt.show()
