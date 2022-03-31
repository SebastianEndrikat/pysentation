
import numpy as np

def titlepage(fig,pres,arg): # define a slide
  # fig is the figure canvas for this slide
  # pres is the instance of the presentation to access certain functions here

  fig.text(0.5,0.6,'Example of using pyplot to create \npresentation slides as image files',
    va='center',ha='center',fontsize=pres.fontSizeLarge)
  fig.text(0.5,0.3,'29. September 2020',va='center',ha='center')

  return

def slide(fig,pres,arg):
  # fig is the figure canvas for this slide
  # pres is the instance of the presentation to access certain functions here
  # Could load data here and plot straight onto the slide.
  # The passed arg can be used to create a bunch of slides that all
  # generally show the same thing but varied in some way that tells a story

  # For this example, interpret arg as a parameter of the plot:
  if np.any(arg==None):
    myVaryingParamter=2.
  else:
    myVaryingParamter=arg      
    fig.text(0.6,0.7,'Dramatic change!')

  pres.title('What a test!')

  thisax=fig.add_axes([0.1,0.15,0.34,0.6]) # x,y,w,h
  thisax.plot([0,1],[myVaryingParamter,1],'k--')
  thisax.set_xlabel('$x$')
  thisax.set_ylabel('$y$',labelpad=10.)
  thisax.set_xlim([0,1])
  thisax.set_ylim([0,3])

  thisax=fig.add_axes([0.6,0.15,0.34,0.6]) # x,y,w,h
  thisax.plot([0,1],[myVaryingParamter,3],'g--')
  thisax.set_xlabel('$x$')
  thisax.set_ylabel('$y$',labelpad=10.)
  thisax.set_xlim([0,1])
  thisax.set_ylim([0,3])

  #pres.printSlideGrid() # for orientation/aligning
  return



