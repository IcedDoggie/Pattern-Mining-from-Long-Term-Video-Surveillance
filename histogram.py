# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:41:32 2017

@author: Ice
"""

def histogram(heatmapArray):
    plt.figure
    hist_Heatmap = cv2.calcHist([heatmapArray], [3], None, [256], [0, 256])
    plt.plot(hist_Heatmap)
    plt.show()