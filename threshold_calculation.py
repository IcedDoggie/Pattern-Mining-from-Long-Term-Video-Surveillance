# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 00:04:41 2017

@author: Ice
"""
from chamfer_distance import chamfer_distance
from calculateSimilarity import calculateSimilarity
import math

def threshold_calculation(training_samples_track, representative_track, nj_parameter):
#    distance = chamfer_distance(training_samples_track, representative_track)
    results_probability = calculateSimilarity(representative_track, training_samples_track, nj_parameter)

    return results_probability