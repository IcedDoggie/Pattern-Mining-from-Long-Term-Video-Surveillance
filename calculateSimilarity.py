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
    
    # influence parameter
    influence = 1
    
    # visualizing anomalous track
    anomalous_track = np.empty([0])
    id_anomalous = np.empty([0])

    while tracks_counter < len(pivot_list) - 1:
        # plotting distance
        distance_array = np.empty([0])

        probability_array = np.empty([0])
        representative_counter = 0
        one_track = new_trajectory[ pivot_list[tracks_counter]:pivot_list[tracks_counter+1] ]
        while representative_counter < len(pivot_list2) - 1: #T'
            nj_param_current_cluster = parameter_nj[representative_counter]
            
            probability = [np.exp( (-nj_param_current_cluster) *
                chamfer_distance(one_track, representative_trajectory[pivot_list2[representative_counter]:pivot_list2[representative_counter+1]]))]         
#            print("probability: " + str(probability))

            # Try plotting the Distance graph
            distance = chamfer_distance(one_track, representative_trajectory[pivot_list2[representative_counter]:pivot_list2[representative_counter+1]])
            distance_array = np.append(distance_array, distance)                    
            
            probability_array = np.append(probability_array, probability)
            representative_counter += 1
#        print("\n")
            
        # distance graph plotting
        min_distance = min(distance_array)
            
        max_probability = np.append(max_probability, min(probability_array)) #verify with dr.john    
        
        threshold_to_compare = np.argmax(probability_array)
        
#        print(threshold_to_compare)        
        if max_probability[tracks_counter] < threshold[threshold_to_compare] and min_distance > 1000:
#        if min_distance > 50000:
            num_anomaly += 1
            print( "min distance: " + str(min_distance))
            # parse the anomalous track data back to anomalydetection

            id_anomalous = np.append(id_anomalous, (one_track.shape[0]))
            anomalous_track = np.append(anomalous_track, (one_track))
        ## calculate comparative likelihood
#        comparative_likelihood = np.append(comparative_likelihood, max_probability[tracks_counter] / threshold[threshold_to_compare])  
#        print("max_prob: " + str(max_probability[tracks_counter]))
#        print("threshold: " + str(threshold[threshold_to_compare]))
        
        temp_num = num_anomaly / (len(pivot_list) - 1)
    
        
        ratio_likelihood_threshold = max_probability[tracks_counter] / threshold[threshold_to_compare] 
        ratio_likelihood_threshold = np.log10(ratio_likelihood_threshold)
#        ratio_likelihood_threshold = max_probability[tracks_counter] * temp_num        
#        print("ratio_likelihood: " + str(ratio_likelihood_threshold))        
        comparative_likelihood = np.append(comparative_likelihood, ratio_likelihood_threshold)            
        
        tracks_counter += 1    
#    print(max_probability)
    return probability, num_anomaly, max_probability, num_new_trajectory, comparative_likelihood, anomalous_track, id_anomalous