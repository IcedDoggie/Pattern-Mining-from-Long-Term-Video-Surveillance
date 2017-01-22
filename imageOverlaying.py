# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:36:21 2017

@author: Ice
"""

def imageOverlaying(imageA, imageB):
    image1 = plt.imread(imageA)
    image2 = plt.imread(imageB)
    imgCombination = image1 + image2
    return imgCombination