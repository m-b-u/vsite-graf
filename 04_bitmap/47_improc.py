""" Simple GUI for demo of imgproc module """


import imgproc
import sys

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from matplotlib.widgets import Button

filename = "../samples/cart_1a34309r.jpg" if len(sys.argv)<2 else sys.argv[1]

class ImageHandlers(object):
    """ Action methods for ImageDialog """

    def __init__(self):
        super(ImageHandlers, self).__init__()
        self.image = None
        self.preview = None

    def do_levels_test(self, event):
        """ Test level adjustments with some predefined settings."""
        self.preview = imgproc.adjust_levels(self.image,
                                             (0.12, 0.8), (0., 1.), 1.0)
        self.update_display()

    def do_autolevels(self, event):
        """ Perform auto levels stretch"""
        self.preview = imgproc.auto_levels(self.image)
        self.update_display()

    def do_blur(self, event):
        """ Perform box blur"""
        self.preview = imgproc.blur_uniform(self.image)
        self.update_display()

    def do_blur_gaussian(self, event):
        """ Perform 3x3 Gaussian blur"""
        self.preview = imgproc.blur_gaussian(self.image)
        self.update_display()

    def do_sharpen(self, event):
        """ Do simple cross sharpen"""
        self.preview = imgproc.sharpen(self.image)
        self.update_display()

    def do_unsharp(self, event):
        """ Do simple unsharp - without masking"""
        self.preview = imgproc.unsharp(self.image)
        self.update_display()

    def do_edges(self, event):
        """ Do simple edge extraction"""
        self.preview = imgproc.edge_hv(self.image)
        self.update_display()

    def apply(self, event):
        """ Apply the current preview image as the new base image"""
        self.image = self.preview.copy()
        self.update_display()

    def reset(self, event):
        """ Reset the preview image to original"""
        self.preview = self.image.copy()
        self.update_display()

    def save(self, event):
        """Save the modified image"""
        pass

    def quit(self, event):
        """ Quit the application."""
        pass

class ImageDialog(ImageHandlers):
    """ Control dialog for image editing actions"""
    def __init__(self):
        """ Initialize dialog and needed data """
        super(ImageDialog, self).__init__()
        self.buttons = []
        self.axes = []
        self.fig = None
        self.image_view = []
        self.filename = None

    def load_file(self, filename):
        """ Load specified file into image buffers"""
        self.filename = filename
        self.image = imgproc.convert_from_uint8(mpimg.imread(filename))
        self.preview = self.image.copy()

    def setup_display(self):
        """ Set up figure for image buffers"""
        self.fig, axis = plt.subplots(2)
        self.image_view = [a.imshow(self.image, aspect=1) for a in axis]
        axis[0].set_title('Image')
        axis[1].set_title('Preview')
        return self.fig, axis, self.image_view

    def setup_controls(self):
        """ Set up button axes"""
        buttons = [('Auto levels', self.do_autolevels),
                   ('Levels1', self.do_levels_test),
                   ('Blur uniform', self.do_blur),
                   ('Blur gaussian', self.do_blur_gaussian),
                   ('Sharpen', self.do_sharpen),
                   ('Unsharp', self.do_unsharp),
                   ('Edge detection', self.do_edges),
                   ('Apply', self.apply),
                   ('Reset', self.reset),
                   ('Save', self.save),
                   ('Quit', self.quit)]
        padding = 0.02
        start, end = 0.1, 0.8
        hspace = (end - start) / len(buttons)
        for i, b in enumerate(buttons):
            axis = self.fig.add_axes([start + i*hspace, 0.03,
                                      start + (i+1)*hspace - padding, 0.03])
            self.axes.append(axis)
            button = Button(axis, b[0])
            button.on_clicked(b[1])
            self.buttons.append(button)

    def run(self):
        """ Start the dialog """
        plt.show()

    def update_display(self):
        """ Update images after some operation """
        self.image_view[0].set_data(self.image)
        self.image_view[1].set_data(self.preview)
        self.fig.canvas.draw_idle()

dlg = ImageDialog()
dlg.load_file(filename)
dlg.setup_display()
dlg.setup_controls()


action_map = {'autolevels': dlg.do_autolevels,
              'levels_test': dlg.do_levels_test,
              'blur': dlg.do_blur,
              'sharpen':  dlg.do_sharpen}

if len(sys.argv)>2:
    fname = sys.argv[2]
    function = action_map.get(fname, None)
    if function:
        print "Perform: ", fname
        function(None)

dlg.run()
