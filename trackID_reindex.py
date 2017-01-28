# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:42:13 2017

@author: Ice

"""
import pandas as pd
import numpy as np

def trackID_reindex(dataframe_to_be_reindexed, currentIndex):
    counter = 1
    
    ## Newly indexed Series
    trackID_Series = dataframe_to_be_reindexed[['TrackID']]
    trackID_Series.loc[0].TrackID = currentIndex
    
    ## reference Series
    ref_Series = dataframe_to_be_reindexed[['TrackID']]
    initial_ID = ref_Series.loc[0].TrackID
    
    while counter < len(dataframe_to_be_reindexed):
        if ref_Series.loc[counter].TrackID == initial_ID:
            trackID_Series.loc[counter].TrackID = currentIndex
        else:
            currentIndex += 1
            trackID_Series.loc[counter].TrackID = currentIndex
            initial_ID = ref_Series.loc[counter].TrackID
        counter += 1
    currentIndex += 1 ##for new document
    dataframe_to_be_reindexed[['TrackID']] = trackID_Series    
    return dataframe_to_be_reindexed, currentIndex