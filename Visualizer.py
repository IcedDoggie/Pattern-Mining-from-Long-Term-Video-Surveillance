# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:38:44 2017

@author: Ice
"""

def Visualizer(list_of_lines, lineColor, filename):
    indices = [0, 1]
    counterForLineConstruction = 0

    #line preparation
    #### Visualize line with Color
    linesegment = mc.LineCollection(list_of_lines, linewidths = 2, linestyles='solid', colors=lineColor)
    #### Visualize line without Color
    # linesegment = mc.LineCollection(dataframeInt, linewidths = 2, linestyles='solid', colors='black')
    #### Visualize an arrow



    #canvas setup
    x = np.arange(641)
    ys = x[0:480, np.newaxis]

    # set plot limits
    ax = plt.axes()
    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(ys.min(), ys.max())
    ax.add_collection(linesegment)
    plt.gca().invert_yaxis()
    im = plt.imread('overlayingImage.png')
    implot = plt.imshow(im)
#     plt.savefig(filename)
    plt.show()
    