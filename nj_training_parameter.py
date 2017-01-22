# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:34:40 2017

@author: Ice
"""

def nj_training_parameter(training_track, representative_track):
    
    # calculate each of the training track chamfer distance
    parameter_nj = []
    training_track, pivot_list = trajectory_pivoting_based_on_id(training_track)
    
    representative_track, pivot_list2 = trajectory_pivoting_based_on_id(representative_track)
    
    # convert to numpy
    training_track = pd.DataFrame.as_matrix(training_track)
    representative_track = pd.DataFrame.as_matrix(representative_track)
    
    tracks_counter = 0
    representative_counter = 0
    
    
    while representative_counter < len(pivot_list2) - 1:
        bottom_param = 0
        while tracks_counter < len(pivot_list) - 1:
            bottom_param += chamfer_distance(training_track[pivot_list[tracks_counter]:pivot_list[tracks_counter + 1]],
                                             representative_track[ pivot_list2[representative_counter]:pivot_list2[representative_counter + 1] ])
            tracks_counter += 1
        if bottom_param >0:    
            combined_param = len(training_track) / bottom_param
        parameter_nj += [combined_param]
        representative_counter += 1
#     print(bottom_param)
    
    return parameter_nj