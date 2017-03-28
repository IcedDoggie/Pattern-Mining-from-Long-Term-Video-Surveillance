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

def calculateSimilarity(representative_trajectory, new_trajectory, parameter_nj, threshold, num_anomaly):
    
    # splitting tracks based on id
    new_trajectory, pivot_list = trajectory_pivoting_based_on_id(new_trajectory)
    num_new_trajectory = len(pivot_list) - 1
    new_trajectory = pd.DataFrame.as_matrix(new_trajectory)   
    
    probability_array = np.empty([0])
    
    tracks_counter = 0
    
    while tracks_counter < num_new_trajectory: #T'
        one_track = new_trajectory[ pivot_list[tracks_counter]:pivot_list[tracks_counter+1] ]
        
        probability = [np.exp( (-parameter_nj) * chamfer_distance(one_track,representative_trajectory))]
        if probability < threshold:
            num_anomaly += 1
        
        probability_array = np.append(probability_array, probability)
        tracks_counter += 1
#        tracks_counter += 1
#     print(parameter_nj)
    print(probability_array)
    return probability, num_anomaly, probability_array, num_new_trajectory