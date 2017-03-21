# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:37:44 2017

@author: Ice
"""

import pandas as pd
import numpy as np


def ColorAssignment(dataframe):

    try:
        dataframe[['ClusterID']]
    except:
#         dataframe = LinesConstruct(dataframe)        
        dataframe = dataframe.rename(columns={'TrackID': 'ClusterID'})
    
#    print(dataframe['ClusterID'].as_matrix())
    dataframe = dataframe['ClusterID'].as_matrix()
    ########################Assign Color##################
    tempColor = np.where(dataframe == 0, 'blue', 
                         np.where( dataframe == 1, 'yellow', 
                                  np.where(dataframe == 2, 'cyan',
                                           np.where(dataframe == 3, 'magenta','black'))))    
    tempColor = np.unique(tempColor)                       
    print(tempColor)
    return tempColor
    ######################################################  