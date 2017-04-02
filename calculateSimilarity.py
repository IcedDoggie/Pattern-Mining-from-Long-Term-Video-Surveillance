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

def calculateSimilarity(representative_trajectory, new_trajectory, parameter_nj, threshold, num_anomaly, comparative_likelihood):
    
    # splitting tracks based on id
    new_trajectory, pivot_list = trajectory_pivoting_based_on_id(new_trajectory)
    num_new_trajectory = len(pivot_list) - 1
    new_trajectory = pd.DataFrame.as_matrix(new_trajectory)   
    representative_trajectory, pivot_list2 = trajectory_pivoting_based_on_id(representative_trajectory) 
    max_probability = np.empty([0])
    representative_trajectory = pd.DataFrame.as_matrix(representative_trajectory)
    representative_counter = 0
#    print(parameter_nj)
#    print(threshold)
#    
    probability_array = np.empty([0])
    threshold_to_compare = 0
    tracks_counter = 0


    while tracks_counter < num_new_trajectory:
        # plotting distance
#        distance_array = np.empty([0])

        probability_array = np.empty([0])
        representative_counter = 0
        one_track = new_trajectory[ pivot_list[tracks_counter]:pivot_list[tracks_counter+1] ]
        while representative_counter < len(pivot_list2) - 1: #T'
            nj_param_current_cluster = parameter_nj[representative_counter]
            
            probability = [np.exp( (-nj_param_current_cluster) *
                chamfer_distance(one_track, representative_trajectory[pivot_list2[representative_counter]:pivot_list2[representative_counter+1]]))]         
#            print("probability: " + str(probability))

            # Try plotting the Distance graph
#            distance = chamfer_distance(one_track, representative_trajectory[pivot_list2[representative_counter]:pivot_list2[representative_counter+1]])
#            distance_array = np.append(distance_array, distance)                    
            
            probability_array = np.append(probability_array, probability)
            representative_counter += 1
#        print("\n")
            
        # distance graph plotting
#        max_distance = np.append(max_distance, max(distance_array))
            
        max_probability = np.append(max_probability, min(probability_array)) #verify with dr.john    
        threshold_to_compare = np.argmax(probability_array)
#        print(threshold_to_compare)        
        if max_probability[tracks_counter] < threshold[threshold_to_compare]:
            num_anomaly += 1
        ## calculate comparative likelihood
#        comparative_likelihood = np.append(comparative_likelihood, max_probability[tracks_counter] / threshold[threshold_to_compare])  
#        print("max_prob: " + str(max_probability[tracks_counter]))
#        print("threshold: " + str(threshold[threshold_to_compare]))
        
        temp_num = num_anomaly / (num_new_trajectory)
    
        
        ratio_likelihood_threshold = max_probability[tracks_counter] / threshold[threshold_to_compare] 
        ratio_likelihood_threshold = np.log10(ratio_likelihood_threshold)
#        ratio_likelihood_threshold = max_probability[tracks_counter] * temp_num        
#        print("ratio_likelihood: " + str(ratio_likelihood_threshold))        
        comparative_likelihood = np.append(comparative_likelihood, ratio_likelihood_threshold)            
        
        tracks_counter += 1    
#    print(max_probability)
    return probability, num_anomaly, max_probability, num_new_trajectory, comparative_likelihood