#!/usr/bin/env python3

# run this to create the example presentation
# individual slides are defined in imported files

from pysentation import presentation
p=presentation('slides') # an instance of the presentation class

# import and create two slides
import example_plot
p.addSlide(example_plot.titlepage)
p.addSlide(example_plot.slide)

# draw the same slide again, but illustrate a change
# the function "slide" interprets arg. In this case as a number.
p.addSlide(example_plot.slide,arg=2.5) 

# import and create another slide
import example_image
p.addSlide(example_image.slide)
