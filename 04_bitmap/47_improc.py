""" Simple GUI for demo of imgproc module """


import imgproc
import sys

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os.path
import sys

from utils import get_component_view

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

    def do_levels_old(self, event):
        """ Test levels with reduced output range """
        self.preview = imgproc.adjust_levels(self.image,
                                             (0., 1.), (0.3, 0.8), 1.0)
        self.update_display()

    def do_levels_clip(self, event):
        """ Test levels with clipped input range """
        self.preview = imgproc.adjust_levels(self.image,
                                             (0.3, 0.8), (0., 1.), 1.8)
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
        basename, ext = os.path.splitext(self.filename)
        num = 1
        out_file = ''
        while True:
            out_file = '%s_%d%s' % (basename, num, ext)
            if os.path.exists(out_file):
                num += 1
            else:
                break
        print("Saving to: %s" % out_file)
        self.save_file(out_file, self.preview)

    def quit(self, event):
        """ Quit the application."""

        sys.exit(0)

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
        self.axishist = []

    def load_file(self, filename):
        """ Load specified file into image buffers"""
        self.filename = filename
        self.image = imgproc.convert_from_uint8(mpimg.imread(filename))
        self.preview = self.image.copy()

    def save_file(self, filename, image):
        """ Save modified buffer to specified filename """
        mpimg.imsave(filename, imgproc.convert_to_uint8(image), vmin=0.0, vmax=0.0)
        
    def setup_display(self):
        """ Set up figure for image buffers"""
        self.fig, axis = plt.subplots(2)
        self.image_view = [a.imshow(self.image, aspect=1) for a in axis]
        axis[0].set_title('Image')
        axis[1].set_title('Preview')

        self.setup_histogram(axis[0], self.image)
        self.setup_histogram(axis[1], self.preview)

        return self.fig, axis, self.image_view


    def setup_histogram(self, axis, data):
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        divider = make_axes_locatable(axis)

        ax2 = divider.new_horizontal(size="30%", pad=0.05)
        #ax2.patch.set_facecolor('black')
        # or ax2.set_axis_bgcolor('black')
        fig1 = axis.get_figure()
        fig1.add_axes(ax2)
        self.axishist.append(ax2)
        self.update_histogram()
        
    def setup_controls(self):
        """ Set up button axes"""
        buttons = [[('Auto levels', self.do_autolevels),
                   ('Levels1', self.do_levels_test),
                   ('Oldie', self.do_levels_old),
                   ('Clip', self.do_levels_clip)],
                   [('Blur uniform', self.do_blur),
                   ('Blur gaussian', self.do_blur_gaussian),
                   ('Sharpen', self.do_sharpen),
                   ('Unsharp', self.do_unsharp),
                   ('Edge detection', self.do_edges)],
                   [('Apply', self.apply),
                   ('Reset', self.reset),
                   ('Save', self.save),
                   ('Quit', self.quit)]]
        max_cols = max(len(row) for row in buttons)
        padding = 0.01
        start, end = 0.03, 0.97
        hspace = (end - start) / max_cols
        row_height = 0.03
        vspace = row_height + 0.003
        for j, row in enumerate(buttons):
            for i, b in enumerate(row):
                box = [start + i*hspace, 0.01 + j*vspace,
                       hspace - padding, row_height]
                print (box)
                axis = self.fig.add_axes(box)

                button = Button(axis, b[0])
                self.axes.append(axis)

                button.on_clicked(b[1])
                self.buttons.append(button)

    def run(self):
        """ Start the dialog """
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        plt.show()

    def update_histogram(self):
        for ax, im in zip(self.axishist, [self.image, self.preview]):
            im_ = get_component_view(im)
            max_ = -1e100;
            ax.cla()

            for comp in ('r', 'g', 'b'):
                n, bin, patches = ax.hist (im_[comp].ravel(), bins=256, histtype='stepfilled', color=comp, edgecolor='none', alpha=1 if comp=='r' else 0.8)
                #min_ = np.min(n[1:-1])
                max_ = max(max_, np.max(n[1:-1]))
                for tl in ax.get_yticklabels():
                    tl.set_visible(False)
            ax.set_ylim(top=max_)

    def update_display(self):
        """ Update images after some operation """
        self.image_view[0].set_data(self.image)
        self.image_view[1].set_data(self.preview)
        self.fig.canvas.draw_idle()
        self.update_histogram()

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
        print(("Perform: ", fname))
        function(None)

dlg.run()
