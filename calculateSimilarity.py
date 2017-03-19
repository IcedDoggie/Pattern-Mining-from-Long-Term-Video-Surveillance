# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:34:21 2017

@author: Ice
"""

from trajectory_pivoting_based_on_id import trajectory_pivoting_based_on_id
from chamfer_distance import chamfer_distance
import pandas as pd
import numpy as np
import math

def calculateSimilarity(representative_trajectory, new_trajectory, parameter_nj):
    
    # splitting tracks based on id
#    representative_trajectory, pivot_list = trajectory_pivoting_based_on_id(representative_trajectory)
#    
#    representative_trajectory = pd.DataFrame.as_matrix(representative_trajectory)

#    tracks_counter = 0
#    probability_array = []
    
    probability_array = np.empty([0])
#    while tracks_counter < len(pivot_list) - 1:
#        probability_array += [math.exp( (-parameter_nj[tracks_counter]) * chamfer_distance(new_trajectory,representative_trajectory[ pivot_list[tracks_counter]:pivot_list[tracks_counter+1] ]))]
        
    for track in new_trajectory: 
        track = track.as_matrix()
        probability = [np.exp( (-parameter_nj) * chamfer_distance(track,representative_trajectory))]
        probability_array = np.append(probability_array, probability)
#        tracks_counter += 1
#     print(parameter_nj)
    print(probability_array)
    return probability