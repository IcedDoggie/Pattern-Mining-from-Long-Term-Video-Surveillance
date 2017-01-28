# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 00:04:41 2017

@author: Ice
"""
from chamfer_distance import chamfer_distance

def threshold_calculation(training_samples_track, representative_track):
    results = chamfer_distance(training_samples_track, representative_track)
    print(results)    