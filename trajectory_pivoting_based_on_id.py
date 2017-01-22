# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:35:05 2017

@author: Ice
"""

def trajectory_pivoting_based_on_id(trajectory_dataframe):
    tempNP_splitter = []
    tempNP_splitter += [0]
    pivot = 0
    pivoted_cluster_id = trajectory_dataframe[['TrackID']].loc[pivot]
    pivoted_cluster_id = pivoted_cluster_id.TrackID
    while pivot < len(trajectory_dataframe):        
        current_cluster_id = trajectory_dataframe[['TrackID']].loc[pivot]
        current_cluster_id = current_cluster_id.TrackID
        if current_cluster_id != pivoted_cluster_id:
            tempNP_splitter += [pivot]
            pivoted_cluster_id = current_cluster_id
        pivot += 1
    tempNP_splitter += [len(trajectory_dataframe)]
    trajectory = trajectory_dataframe[['X','Y']]        
    return trajectory, tempNP_splitter