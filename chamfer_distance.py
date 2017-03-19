# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:35:33 2017

@author: Ice
"""
from trajectory_pivoting_based_on_id import trajectory_pivoting_based_on_id
import numpy as np
import pandas as pd

def chamfer_distance(track_p, track_q):
    # track q -> examplar/representative track
    first_term = ( 1 / abs(len(track_p)) )
    
    # find how many representative track in track_q and pivot it
    track_q, pivot_list = trajectory_pivoting_based_on_id(track_q)
    # pivot list is where how many places and where should we pivot,
    # hence, by getting  (pivot num - 1), logically we can know how many id exists
    num_track_q = len(pivot_list) - 1
    track_q = pd.DataFrame.as_matrix(track_q)    
    
    difference_tp_tq = []
    check_min_tp_tq = []
    tracks_counter = 0
#    print(track_p)
    
    # check for each representative track(loop), and get the minimum 
    # doesnt need to loop track_p/new track because it's handled by trajectoryclus
    while tracks_counter < num_track_q:
        one_representative_track = track_q[ pivot_list[tracks_counter]:pivot_list[tracks_counter+1] ]
        
        second_term_value = 0
        for points in one_representative_track:  
            # loop through every point in representative track
            temp_dist = abs(np.subtract(track_p[:,0], points[0]))     
            temp_dist2 = abs(np.subtract(track_p[:,1], points[1]))
            temp_dist = np.add(temp_dist, temp_dist2)
            temp_dist = np.power(temp_dist, 2)
            second_term_value += temp_dist
        second_term_value = sum(second_term_value) #sum all vals in temp_dist array
#        print("second_term_value")  
#        print(second_term_value)
        check_min_tp_tq += [second_term_value]
        tracks_counter += 1
    
#    print(min(check_min_tp_tq))
    
        
    second_term = min(check_min_tp_tq)  
    
    distance = first_term * second_term
#    print(distance)
    return distance