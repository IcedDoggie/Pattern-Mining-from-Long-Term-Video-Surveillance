# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 15:44:35 2017

@author: Ice
"""

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

def trainSimilarity(representative_trajectory, new_trajectory, parameter_nj):
    
    # splitting tracks based on id
    new_trajectory, pivot_list = trajectory_pivoting_based_on_id(new_trajectory)
    num_new_trajectory = len(pivot_list) - 1
    new_trajectory = pd.DataFrame.as_matrix(new_trajectory)   
    representative_trajectory, pivot_list2 = trajectory_pivoting_based_on_id(representative_trajectory) 
    threshold_array = np.empty([0])
    representative_trajectory = pd.DataFrame.as_matrix(representative_trajectory)
    representative_counter = 0
    while representative_counter < len(pivot_list2) - 1:
        probability_array = np.empty([0])
        tracks_counter = 0
        nj_param_current_cluster = parameter_nj[representative_counter]
        while tracks_counter < num_new_trajectory:
            one_track = new_trajectory[ pivot_list[tracks_counter]:pivot_list[tracks_counter+1] ]
            
            probability = [np.exp( (-nj_param_current_cluster) *
                chamfer_distance(one_track, representative_trajectory[pivot_list2[representative_counter]:pivot_list2[representative_counter+1]]))]
            probability_array = np.append(probability_array, probability)
            tracks_counter += 1
        threshold_array = np.append(threshold_array, min(probability_array)) #verify with dr.john    
#        tracks_counter += 1
        representative_counter += 1
#     print(parameter_nj)
#    print(probability_array)
    return threshold_array