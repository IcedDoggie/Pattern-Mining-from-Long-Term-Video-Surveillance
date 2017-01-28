# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:35:33 2017

@author: Ice
"""
import numpy as np

def chamfer_distance(track_p, track_q):
     
    first_term = ( 1 / abs(len(track_p)) )

    difference_tp_tq = []
    for points in track_p:
        temp_dist = np.subtract(track_q[:,0], points[0])
        temp_dist2 = np.subtract(track_q[:,1], points[1])
        temp_dist = np.add(temp_dist, temp_dist2)
        temp_dist = np.power(temp_dist, 2)
        temp_dist = min(temp_dist)
        difference_tp_tq += [temp_dist]
#     print(difference_tp_tq)
    second_term = sum(difference_tp_tq)    
    
    distance = first_term * second_term
    
#     print(distance)
    return distance