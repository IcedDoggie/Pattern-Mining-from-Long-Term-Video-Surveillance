# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:41:43 2017

@author: Ice
"""

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0, 0, 0])

def constructHeatmap(heatmapDataInput): 
    heatmapData = heatmapDataInput[['X','Y']]
    heatmapData = pd.DataFrame.as_matrix(heatmapData)
    heatmapData_X = heatmapDataInput[['X']]
    heatmapData_Y = heatmapDataInput[['Y']]
    heatmapData_X = pd.DataFrame.as_matrix(heatmapData_X)
    heatmapData_X = heatmapData_X.flatten()
    heatmapData_Y = pd.DataFrame.as_matrix(heatmapData_Y)
    heatmapData_Y = heatmapData_Y.flatten()
    
    heatmapData = heatmapData.flatten()

    #insert data for scaling the heatmap
    heatmapData_X = np.insert(heatmapData_X, [0], 0) #Min cap
    heatmapData_X = np.append(heatmapData_X, 640) #Max cap
    heatmapData_Y = np.insert(heatmapData_Y, [0], 0) #Min cap
    heatmapData_Y = np.append(heatmapData_Y, 480) #Max cap
    xmin = 0
    xmax = 640
    ymin = 0
    ymax = 480
    
    ########### hexbin approach ##########
#     %matplotlib notebook
# #     dataHeat = plt.hexbin(heatmapData_X, heatmapData_Y, gridsize=(640,480), xscale='linear', yscale='linear')
#     dataHeat = plt.hexbin(heatmapData_X, heatmapData_Y)
#     plt.axis([xmin, xmax, ymin, ymax])
# #     plt.colorbar()
#     plt.gca().invert_yaxis()
#     plt.savefig('heatmap.png')
    ######################################
    
    ########## try histogram2d approach ############
    dataHistogram = np.histogram2d(heatmapData_X, heatmapData_Y, bins=[640,480])
    ###########################################

    ##################### Overlaying image #########################
#     %matplotlib notebook
#     imageA = cv2.imread("heatmap.png")
#     dim = (640, 480)
#     imageA = cv2.resize(imageA, dim)
#     imageB = cv2.imread("overlayingImage.png")
#     imageC = cv2.add(imageA, imageB)
#     cv2.imshow("heatmap", imageC)
#     cv2.waitKey(0)
    return dataHistogram[0]
