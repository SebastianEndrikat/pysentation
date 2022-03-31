



def slide(fig,pres,arg):
  # fig is the figure canvas for this slide
  # pres is the instance of the presentation to access certain functions here

  pres.title('Embedding an image file')

  pres.embeddImage('exampleImage.png',x=0.5,y=0.3,scale=3.)
  fig.text(0.5,0.4,'Clearly the coolest drawing ever',ha='right',rotation=45)

  #pres.printSlideGrid() # for orientation/aligning
  return