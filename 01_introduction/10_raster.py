import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np

def demo_imagerepresentation(xres, yres):
	im = np.zeros ((yres, xres),dtype=np.uint8)
	im[2,3] = 255

	fig = plt.figure(1)
	plot = fig.add_subplot(1,1,1)	
	ax = plot.imshow(im, cm.gray, interpolation = 'none')
	plt.show()

	# represent same data as 1D array
	im_linear = im.ravel()
	# turn the first 'pixel' on
	im_linear[0] = 255
        # turn the last 'pixel' on
	im_linear[-1] = 64
        
        im[5,3] = 255
        im[5,4] = 200

	fig, axis = plt.subplots(2)
	axis[0].imshow(im, cm.gray, interpolation = 'none')
        axis[0].set_title('2D view')
        axis[1].imshow(im.reshape(1, -1), cm.gray, interpolation = 'none', aspect = 7)
        axis[1].get_yaxis().set_visible(False)
        axis[1].set_title('1D view')
	
	plt.show()




if __name__=='__main__':

	print "Part 1 - Image as number array"
	demo_imagerepresentation(20, 10)


	print "End"
