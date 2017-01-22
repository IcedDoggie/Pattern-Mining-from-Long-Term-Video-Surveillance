# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:37:44 2017

@author: Ice
"""

def ColorAssignment(dataframe):

    try:
        dataframe[['ClusterID']]
    except:
#         dataframe = LinesConstruct(dataframe)        
        dataframe = dataframe.rename(columns={'TrackID': 'ClusterID'})
    

    ########################Assign Color##################
    tempColor = np.where(dataframe['ClusterID'] == 0, 'blue', 
                         np.where( dataframe['ClusterID'] == 1, 'yellow', 
                                  np.where(dataframe['ClusterID'] == 2, 'cyan',
                                           np.where(dataframe['ClusterID'] == 3, 'magenta','black'))))    
    counter = 1
    helper_color = tempColor[0]
    tempColor2 = []
    tempColor2 += [helper_color]
    while counter < len(tempColor):
        if helper_color != tempColor[counter]:
            tempColor2 += [tempColor[counter]]
            helper_color = tempColor[counter]
        counter += 1

    return tempColor2
    ######################################################  