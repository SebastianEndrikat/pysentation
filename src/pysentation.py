#!/usr/bin/env python3


import os
import errno
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
plt.style.use(os.path.dirname(__file__)+'/mplstyle')  # file in this dir


class presentation:
    ''' Add slides to an instance of this class and then render them all here'''

    def __init__(self, outDir, showSlideNo=True, fileEnding='png'):
        self.slideCounter = 0  # counter of the slides
        self.slideNo = 0  # counter of the visual page number
        self.showSlideNo = showSlideNo  # show the page number
        self.fileEnding = fileEnding

#        # if serif:
#        self.fontSize=22
#        self.fontSizeLarge=34
#        self.fontSizeSmall=16 # 18

        # if sans-serif:
        self.fontSize = 20
        self.fontSizeLarge = 32
        self.fontSizeSmall = 16

        self.mkdir(outDir)
        self.outDir = outDir

        # widescreen format 16:9. change slide size here
#        self.slideWidth=13.333 # inches
        self.slideWidth = 13.34  # inches such that even number of pixel
        self.slideHeight = 7.5  # inches
        self.dpi = 300  # image resolution in dots per inch

        return

    def changeOutDir(self, newOutDir):
        self.mkdir(newOutDir)
        self.outDir = newOutDir
        return

    def resetSlideNo(self):
        # will overwrite slides if the outDir is still the same
        self.slideCounter = 0  # counter of the slides
        self.slideNo = 0  # counter of the visual page number
        return

    def addSlide(self, slide, arg=None, newSlideNo=True, render=True):
        ''' Add a slide to the presentation

        Slide is a function
        Set newSlideNo=False if the slide number should be the same as on the previous slide
        render=False is a dry run, only returning the file name
        '''

        outFile = self.outDir+'/slide%04i.' % self.slideCounter + self.fileEnding

        if newSlideNo:
            self.slideNo += 1
        if render:
            fig = plt.figure(figsize=(self.slideWidth, self.slideHeight))
            self.fig = fig  # current slide canvas
            # execute the passed function to populate the slide
            slide(fig, self, arg)

            if self.showSlideNo:
                # dont write slide number as a fraction of the total. It makes people look forward to the end.
                fig.text(0.95, 0.03, '%i' % self.slideNo, va='bottom',
                         ha='right', fontsize=self.fontSizeSmall)
            if outFile[-3:] == 'pdf':
                plt.savefig(outFile)
            else:
                # maybe jpg would be smaller than png? requires pillow
                plt.savefig(outFile, dpi=self.dpi)
            plt.close()
            print('Wrote '+outFile)
        else:
            if not os.path.exists(outFile):
                print('WARNING: Did not write even tho it does not exist: '+outFile)
                # even if the warning doesnt go off, it could of course be a wrong
                # slide with the correct name...

        self.slideCounter += 1
        return outFile

    def embeddImage(self, theFile, x, y, scale=1., w=None, h=None, anchor='SW', thisax=None):
        ''' Put an image on the slide

        x,y is the lower left corner in fractions of page size
        if w,h are not None, but instead width, height in fractions of the slide, scale is ignored
          parts of w,h will be ignored depening on the anchor, to keep the aspect ratio correct
        '''

        im = mpimg.imread(theFile)
        if (not w == None) and (not h == None):
            thisax = self.fig.add_axes([x, y, w, h])
            thisax.axis('off')
        if thisax == None:
            shape = im.shape
            nx = shape[0]
            ny = shape[1]
            Lx = nx/float(self.dpi)  # x-extent of the image in inches
            Ly = ny/float(self.dpi)  # y-extent of the image in inches
            Lx /= self.slideWidth  # x-extent of the imege in fraction of the slide
            Ly /= self.slideHeight  # y-extent of the imege in fraction of the slide
            Lx *= scale
            Ly *= scale
            if anchor == 'SW':
                x = x
                y = y
            elif anchor == 'C':
                # Still defining the SW corner
                x -= (Lx/2.)
                y -= (Ly/2.)
            else:
                raise ValueError('Anchor for embeddImage not defined')
            thisax = self.fig.add_axes([x, y, Lx, Ly])  # x,y,w,h
            thisax.axis('off')
        thisax.imshow(im)
        # so that the passed x,y marks the lower left corner
        thisax.set_aspect('equal', adjustable='box', anchor=anchor)
        # possible anchors: N,W,S,E, C, NW,NE,SW,SW. but this is just within the axes
        return thisax

    def drawArrow(self, x0, y0, x1, y1, color='k', lw=2., ls='-', ec=None, thisax=None, coords='axes fraction'):
        if ec == None:
            ec = color
        if thisax == None:
            # x,y are in fractions of the slide width/height
            thisax = self.fig.add_axes([0, 0, 1., 1.])  # x,y,w,h
            thisax.axis('off')
        thisax.annotate('', xy=(x1, y1),
                        xycoords=coords,  # not 'data'
                        xytext=(x0, y0),
                        textcoords=coords,
                        arrowprops=dict(
            #            arrowstyle= '->',
                        arrowstyle='simple',
                        color=color, lw=lw, ls=ls, ec=ec))
        return thisax

    def printSlideGrid(self):
        ''' Print a grid on the current slide for aligning '''

        thisax = self.fig.add_axes([0., 0., 1., 1.])  # x,y,w,h
        thisax.axis('off')
        thisax.set_xlim([0, 1])
        thisax.set_ylim([0, 1])
        for x in [0.25, 0.5, 0.75]:
            thisax.plot([x, x], [0, 1], 'k-')
        for y in [0.25, 0.5, 0.75]:
            thisax.plot([0, 1], [y, y], 'k-')
        return

    def title(self, theStr, x=0.05, y=0.9):  # change default postion here
        ''' Add a title to a slide of this presentation '''
        self.fig.text(x, y, theStr, va='center', ha='left',
                      fontsize=self.fontSizeLarge)
        return

    def mkdir(self, thedir):
        try:
            os.makedirs(thedir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
