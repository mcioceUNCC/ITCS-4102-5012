#   File: invertColor.py
#   Date: 10/12/18
#   Author: Mike Cioce
#   Purpose: This program accepts a user image as input. It then processes
#       the image to invert the color of the image, returning an image with
#       a 'negative' effect.

import matplotlib.pyplot
import matplotlib.image
import numpy

# get the file name and directory path from the user

fileName = input("Enter the file path to an image here: ")
print(fileName)

#now read in the image
imageFile = matplotlib.image.imread(fileName)
print(imageFile)

#get the dimensions of the imageFile:

for x in numpy.nditer(imageFile, op_flags=["readwrite"]):
    #print(x)
    x[...] = 1 - x
    #print(x[...])
print(imageFile)
matplotlib.pyplot.imsave("output.png",imageFile,format="png")
