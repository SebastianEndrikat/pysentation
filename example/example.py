#!/usr/bin/env python3

# run this to create the example presentation
# individual slides are defined in imported files

import sys
sys.path.insert(0, '../src')
from pysentation import presentation
p = presentation('slides')  # an instance of the presentation class

# import and create two slides
import example_plot
p.addSlide(example_plot.titlepage, render=True)
# set render to False if no changes made to save time running this
p.addSlide(example_plot.slide, render=True)

# draw the same slide again, but illustrate a change
# the function "slide" uses arg. In this case as a number.
p.addSlide(example_plot.slide, arg=2.5, render=True)

# import and create another slide
import example_image
p.addSlide(example_image.slide, render=True)
