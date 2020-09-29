#!/usr/bin/env python3


import numpy as np
import os
import errno
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
plt.style.use('mplstyle') # file in this dir




class presentation:
  # add slides to an instance of this class and then render them all here

  def __init__(self,outDir,showSlideNo=True):
    self.slideCounter=0 # counter of the slides
    self.slideNo=0 # counter of the visual page number
    self.showSlideNo=showSlideNo # show the page number

    self.fontSize=22
    self.fontSizeLarge=34
    self.fontSizeSmall=18

    self.mkdir(outDir)
    self.outDir=outDir

    # widescreen format 16:9. change slide size here
    self.slideWidth=13.333 # inches
    self.slideHeight=7.5 # inches
    self.dpi=300 # image resolution in dots per inch

    return

  def addSlide(self,slide,arg=None,newSlideNo=True):
    # slide is a function
    # set newSlideNo=False if the slide number should be the same as on the previous slide


    fig=plt.figure(figsize=(self.slideWidth, self.slideHeight))
    self.fig=fig # current slide canvas
    slide(fig,self,arg) # execute the passed function to populate the slide

    if newSlideNo:
      self.slideNo +=1
    if self.showSlideNo:
      # dont write slide number as a fraction of the total. It makes people look forward to the end.
      fig.text(0.95,0.03,'%i' %self.slideNo, va='bottom',ha='right',fontsize=self.fontSizeSmall)
    plt.savefig(self.outDir+'/slide%04i.png' %self.slideCounter,dpi=self.dpi) # maybe jpg would be smaller? requires pillow
    self.slideCounter +=1
    return

  def embeddImage(self,theFile,x,y,scale=1.):
    # put an image on the slide
    # x,y is the lower left corner in fractions of page size
    im=mpimg.imread(theFile)
    shape=im.shape
    nx=shape[0]; ny=shape[1]
    Lx=nx/float(self.dpi) # x-extent of the image in inches
    Ly=ny/float(self.dpi) # y-extent of the image in inches
    Lx /= self.slideWidth # x-extent of the imege in fraction of the slide
    Ly /= self.slideHeight# y-extent of the imege in fraction of the slide
    Lx*=scale
    Ly*=scale
    thisax=self.fig.add_axes([x,y,Lx,Ly]) # x,y,w,h
    thisax.axis('off')
    thisax.imshow(im)
    thisax.set_aspect('equal', adjustable='box', anchor='SW') # so that the passed x,y marks the lower left corner
    return

  def printSlideGrid(self):
    # print a grid on the current slide for aligning
    
    thisax=self.fig.add_axes([0.,0.,1.,1.]) # x,y,w,h
    thisax.axis('off')
    thisax.set_xlim([0,1])
    thisax.set_ylim([0,1])
    for x in [0.25,0.5,0.75]:
      thisax.plot([x,x],[0,1],'k-')
    for y in [0.25,0.5,0.75]:
      thisax.plot([0,1],[y,y],'k-')
    return

  def title(self,theStr,x=0.05,y=0.9): # change default postion here
    # add a title to a slide of this presentation
    self.fig.text(x,y,theStr,va='center',ha='left',fontsize=self.fontSizeLarge)
    return



  def mkdir(self,thedir):
    try:
        os.makedirs(thedir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise



