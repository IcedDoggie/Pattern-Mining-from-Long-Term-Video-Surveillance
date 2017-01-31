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
    track_q = pd.DataFrame.as_matrix(track_q)    
    
    difference_tp_tq = []
    check_min_tp_tq = []
    tracks_counter = 0
#    print(track_p)
    while tracks_counter < len(track_q):
#        print(track_q[tracks_counter])        
#        for points in track_q[tracks_counter]:
#        print(points)
#        print("x: ")
#        print(points[0])
        point = track_q[tracks_counter]
#        print("point: ")        
#        print(point[0])
#        print(type(point[0]))
        temp_dist = np.subtract(point[0], track_p[:,0])
#        print("here1")
        
        temp_dist2 = np.subtract(point[1], track_p[:,1])
#        print("here2")

        temp_dist = np.add(temp_dist, temp_dist2)
#        print("here3")

        temp_dist = np.power(temp_dist, 2)
        check_min_tp_tq += [temp_dist]
        tracks_counter += 1
#    print(check_min_tp_tq)
    counter = 0
    while counter < len(check_min_tp_tq):
        temp_dist = min(check_min_tp_tq[counter])
        counter += 1
    difference_tp_tq += [temp_dist]
        
    #backup
#    for points in track_p:
#        temp_dist = np.subtract(track_q[:,0], points[0])
#        temp_dist2 = np.subtract(track_q[:,1], points[1])
#        temp_dist = np.add(temp_dist, temp_dist2)
#        temp_dist = np.power(temp_dist, 2)
#        temp_dist = min(temp_dist)
#        difference_tp_tq += [temp_dist]
#     print(difference_tp_tq)
    second_term = sum(difference_tp_tq)    
    
    distance = first_term * second_term
    
#    print(distance)
    return distance