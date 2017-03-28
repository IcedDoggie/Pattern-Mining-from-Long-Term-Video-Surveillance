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
#    print(track_q.loc[0])
      
    second_term_sum = np.empty([0])
    check_min_tp_tq = np.empty([0])
    tracks_counter = 0
#    print(track_p)
    
    # check for each representative track(loop), and get the minimum 
    # doesnt need to loop track_p/new track because it's handled by trajectoryclus
    while tracks_counter < len(track_p):
        # Xj        
        second_term_value = 0
        representative_counter = 0
        while representative_counter < len(track_q):
            # loop through every point in representative track
            temp_dist = abs(np.subtract(track_p[tracks_counter,0], track_q[representative_counter,0]))     
            temp_dist2 = abs(np.subtract(track_p[tracks_counter,1], track_q[representative_counter,1]))
            temp_dist = np.add(temp_dist, temp_dist2)
            temp_dist = np.power(temp_dist, 2)
            check_min_tp_tq = np.append(check_min_tp_tq, temp_dist)
            representative_counter += 1
            #sum all vals in temp_dist array
        
        second_term_sum = np.append(second_term_sum, min(check_min_tp_tq))
        tracks_counter += 1
    
#    print(min(check_min_tp_tq))
    second_term_value = sum(second_term_sum)
        
    
    distance = first_term * second_term_value
#    print(distance)
    return distance