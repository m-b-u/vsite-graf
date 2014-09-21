import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.cm as cm
import numpy as np


if __name__=='__main__':

	im = np.zeros ((16,16),dtype=np.uint8)
	im[2,2] = 200
	fig = plt.figure(1)

	plot = fig.add_subplot(1,1,1)	

	plot.imshow(im, cm.gray, interpolation = 'none')

	plt.show()
	print "Part 2"

	xres = 20
	yres = 20

#	im_r = np.zeros ((64,64),dtype=np.uint8)
#	im_g = np.zeros ((64,64),dtype=np.uint8)
#	im_b = np.zeros ((64,64),dtype=np.uint8)

	im_r = np.linspace (255, 0, num=xres*yres, endpoint=True) 
	im_r.shape = (xres,yres)
	im_g = np.linspace (0, 255, num=xres*yres, endpoint=True) 
	im_g.shape = (xres,yres)
	im_b = np.linspace (128, 384, num=xres*yres, endpoint=True) 
	im_b.shape = (xres,yres)
	im_b= im_b.transpose()

	im_rgb = np.zeros((xres,yres,3), dtype=np.uint8)

	im_rgb[...,0] = im_r
	im_rgb[...,1] = im_g
	im_rgb[...,2] = im_b

	fig = plt.figure(2, (8., 8.)) 
	grid = ImageGrid(fig, 222, # similar to subplot(111)
	                nrows_ncols = (2, 2), # creates 2x2 grid of axes
	                axes_pad = 0.1, # pad between axes in inch.
	                )

	im_grid = [im_r, im_g, im_b, im_rgb]

	for i in range(3):   # Do not show the composite image yet
		cmap = cm.gray if i < 3 else None
		grid[i].imshow(im_grid[i], cmap = cmap, interpolation = 'none') # The AxesGrid object work as a list of axes.

	plt.show()

	print "Part 3"

	fig = plt.figure(3, (8., 8.)) 
	grid = ImageGrid(fig, 222, # similar to subplot(111)
	                nrows_ncols = (2, 2), # creates 2x2 grid of axes
	                axes_pad = 0.1, # pad between axes in inch.
	                )

	cm_red = LinearSegmentedColormap.from_list('cm_black_red', [cm.colors.cnames['black'], cm.colors.cnames['red']]) 
	cm_green = LinearSegmentedColormap.from_list('cm_black_green', [cm.colors.cnames['black'], cm.colors.cnames['green']])
	cm_blue= LinearSegmentedColormap.from_list('cm_black_blue', [cm.colors.cnames['black'], cm.colors.cnames['blue']])

	color_maps = [cm_red, cm_green, cm_blue, None]

	for i in range(4):
		cmap = color_maps[i]
		grid[i].imshow(im_grid[i], cmap = cmap, interpolation = 'none') # The AxesGrid object work as a list of axes.


	plt.show()

	print "End"