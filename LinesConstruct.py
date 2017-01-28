# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:37:52 2017

@author: Ice
"""
import pandas as pd
import numpy as np

# Construct lines for visualization in plot
def LinesConstruct(dataFrameSelected):
    concatenator = dataFrameSelected[['TrackID','X','Y']]
    concatenator2 = dataFrameSelected[['X', 'Y']]

    row_iterator = concatenator.iterrows()
    row_id, this_row = next(row_iterator)
    #slicing dataframe to respective arrays for LineCollection function
    initialID = this_row['TrackID']
    slicingArray = []
    for i, rows in row_iterator:
        if rows['TrackID'] != initialID:
            slicingArray.append(i)
            initialID = rows['TrackID']

    testChamp = np.split( concatenator2, slicingArray )
    testChampSize = len(testChamp)
    dummyTest2 = list(testChamp)
    return dummyTest2