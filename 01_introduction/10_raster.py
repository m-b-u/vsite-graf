import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.cm as cm
import numpy as np

def demo_imagerepresentation(xres, yres):
	im = np.zeros ((xres, yres),dtype=np.uint8)
	im[2,2] = 255

	fig = plt.figure(1)
	plot = fig.add_subplot(1,1,1)	
	ax = plot.imshow(im, cm.gray, interpolation = 'none')
	plt.show()

	# represent same data as 1D array
	im_linear = im.ravel()
	# turn the first 'pixel' on
	im_linear[0] = 255
	im_linear[-1] = 64

	fig = plt.figure()
	plot = fig.add_subplot(1,1,1)	
	ax = plot.imshow(im, cm.gray, interpolation = 'none')
	

	plt.show()

def generate_gradient_components(xres, yres):

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

	# alternative:
	#  im_rgb = np.zeros((xres, yres, 3), dtype=np.uint8)
	#  im=im_rgb.view(dtype=[('r', 'u1'), ('g', 'u1'), ('b', 'u1')]) [:,:,0]
	#  im['r'] = .......

	return im_r, im_g, im_b, im_rgb


def demo_components(im_r, im_g, im_b, im_rgb):
	fig = plt.figure(2) 
	grid = ImageGrid(fig, 222, 
	                nrows_ncols = (2, 2), # creates 2x2 grid of axes
	                axes_pad = 0.1, # pad between axes in inch.
	                )

	im_grid = [im_r, im_g, im_b, im_rgb]

	for i in range(3):   # Do not show the composite image yet
		cmap = cm.gray if i < 3 else None
		grid[i].imshow(im_grid[i], cmap = cmap, interpolation = 'none') # The AxesGrid object work as a list of axes.

	plt.show()

def demo_compositing(im_r, im_g, im_b, im_rgb):
	fig = plt.figure(3) 
	grid = ImageGrid(fig, 222, # similar to subplot(111)
	                nrows_ncols = (2, 2), # creates 2x2 grid of axes
	                axes_pad = 0.1, # pad between axes in inch.
	                )

	cm_red = LinearSegmentedColormap.from_list('cm_black_red', [cm.colors.cnames['black'], cm.colors.cnames['red']]) 
	cm_green = LinearSegmentedColormap.from_list('cm_black_green', [cm.colors.cnames['black'], cm.colors.cnames['green']])
	cm_blue= LinearSegmentedColormap.from_list('cm_black_blue', [cm.colors.cnames['black'], cm.colors.cnames['blue']])

	im_grid = [im_r, im_g, im_b, im_rgb]

	color_maps = [cm_red, cm_green, cm_blue, None]

	for i in range(4):
		cmap = color_maps[i]
		grid[i].imshow(im_grid[i], cmap = cmap, interpolation = 'none') # The AxesGrid object work as a list of axes.


	plt.show()



if __name__=='__main__':

	print "Part 1 - Image as number array"
	demo_imagerepresentation(24, 16)

	print "Part 2 - Color image components"

	im_r, im_g, im_b, im_rgb = generate_gradient_components(20, 20)

	demo_components(im_r, im_g, im_b, im_rgb)
	
	print "Part 3 - Color image compositing"

	demo_compositing(im_r, im_g, im_b, im_rgb)

	print "End"