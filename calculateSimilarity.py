# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:34:21 2017

@author: Ice
"""

def calculateSimilarity(representative_trajectory, new_trajectory, parameter_nj):
    
    # splitting tracks based on id
    representative_trajectory, pivot_list = trajectory_pivoting_based_on_id(representative_trajectory)
    
    representative_trajectory = pd.DataFrame.as_matrix(representative_trajectory)

    tracks_counter = 0
    probability_array = []
    
#         print((representative_trajectory[ tempNP_splitter[tracks_counter]:tempNP_splitter[tracks_counter+1] ]))
#         print(tracks)
#     for each in parameter_nj:
    while tracks_counter < len(pivot_list) - 1:
        probability_array += [math.exp( (-parameter_nj[tracks_counter]) * chamfer_distance(new_trajectory,representative_trajectory[ pivot_list[tracks_counter]:pivot_list[tracks_counter+1] ]))]
        tracks_counter += 1
#     print(parameter_nj)
    print(probability_array)
    return max(probability_array)