# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 15:02:07 2017

@author: Ice
"""

import pandas as pd
import numpy as np
import cv2
from sklearn.cluster import KMeans
from pandas import Series, DataFrame, Panel
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import matplotlib.image as mpimg
from matplotlib import collections as mc 
import os
import argparse
import sys
import subprocess
import math
from datetime import datetime
from DirectionCalculation import calculateGradient, calculateVector
from calendarFunction import calendarFunction
from chamfer_distance import chamfer_distance
from ColorAssignment import ColorAssignment
from LinesConstruct import LinesConstruct
from nj_training_parameter import nj_training_parameter
from ReadTraclusExport import ReadTraclusExport
from trackID_reindex import trackID_reindex
from TraClusFileExporter import TraClusFileExporter
from trajectory_pivoting_based_on_id import trajectory_pivoting_based_on_id
from TrajectoryID_Extraction import TrajectoryID_Extraction
from calculateSimilarity import calculateSimilarity
from Visualizer import Visualizer
from threshold_calculation import threshold_calculation
from runTraClus import runTraClus
from anomaly_detection import anomaly_detection

import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

##################################### Tunable Variables ###########################################
# days_to_process = 7
pd.options.display.max_rows = 100
###################################################################################################

    ###############################string concatenation & Load Data########################
def TrajectoryClustering_Traclus(traFileCreation, day_to_analyze):
    #####################################string variables##############################################
    dayArray = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17'
    ,'18','19','20','21','22','23','24','25','26','27','28','29','30','31']
    monthArray = ['01','02','03','04','05','06','07','08','09','10','11','12',]
    # Tunable Variables
    # currentYear = 2013 # input 1
    # pointerMonth = n n1	   # input 2
    # pointerDay = 0   # input 3
    
    currentYear = 2012
    currentMonth = monthArray[0]
    currentDay = dayArray[0]
    pointerMonth = 0
    pointerDay = 0
    daysToChoose = 30 #30 for original experiment
    cycle_loop = 5
    cycle_counter = 0
    listDay = []
    
    # analyzing based on day of each week
    mondayList = []
    tuesdayList = []
    wednesdayList = []
    thursdayList = []
    fridayList = []
    saturdayList = []
    sundayList = []
    counter_listDay = 0
#    day_to_analyze = 2 #0 - monday, 6 - sunday #can prompt for input later
    allFrames = pd.DataFrame() #this is to get back the trajectory for calculating threshold
    
    # probability calculation
    threshold = np.empty([0])
    
    #####################################################################################################    
    
    currentIndex = 1 # This variable is used to reindex every dataframe
    while cycle_counter < cycle_loop:    
        counter = 0
        frames = pd.DataFrame()  
        os.chdir('E:\Documents\MMU Studies\Python Scripts\Track LOST dataset')
        col_names = ['TrackID', 'FrameNo', 'X', 'Y']
        print(os.getcwd())
        while counter < daysToChoose:
            stringDate = '001_' + str(currentYear) + str(currentMonth) + str(currentDay) + '.txt' 
            date = str(currentYear) + str(currentMonth) + str(currentDay)
#            print(date)
            string_to_be_parsed = "pd.read_table('" + stringDate + "',delimiter=' ', header=None, names=col_names)"
            datetime_convert = datetime.strptime(date, '%Y%m%d')
            dayInWeek = datetime_convert.weekday()
#            exec("%s%d = %s" % ("day", counter, string_to_be_parsed))
            try:
                exec("%s%d = %s" % ("day", counter, string_to_be_parsed))
                tempString_Date = eval("%s%d" % ("day", counter))   
                tempString_Date, currentIndex = trackID_reindex(tempString_Date, currentIndex)
                if dayInWeek == day_to_analyze:
                    frames = frames.append(tempString_Date)
#                print("Yes!")
            except:
                counter -= 1
#                print("Nope!")
            counter += 1
    
            currentYear, currentMonth, currentDay, pointerMonth, pointerDay = calendarFunction(currentYear, currentMonth, currentDay, pointerMonth, pointerDay)
            
            # export tra file for one day
            filename = "Day_" + str(day_to_analyze) + "_" + str(cycle_counter) + ".tra"
#            filename = "All_days_" + str(day_to_analyze) + ".txt" 
    #         TraClusFileExporter(tempString_Date, filename)
    #     #######################################################################################
    
        
        # concatDay = pd.concat(frames, ignore_index=True) #this shud be removed cuz frames no longer is np array, it's pd df now.
        concatDay = frames.sort_values(by='TrackID', ascending=True)
        allFrames = allFrames.append(concatDay)
        concatDay = concatDay.reset_index(drop=True)
        
    #    print(concatDay)
        os.chdir('E:\Documents\MMU Studies\Python Scripts')
        cycle_counter += 1
    #     ####################################File Preparation###########################################
        if traFileCreation == True:        
            filename = "30_days_" + str(cycle_counter) + "_loop_" + str(day_to_analyze) + ".tra"
            TraClusFileExporter(concatDay, filename)
        ###############################################################################################
        
    ####################################Visualizing Multiple##########################################
    
    visualize_num = 5
    visualize_count = 0
    inner_loop_count = 0
    
    #### runTraClus ####
    if traFileCreation == True:
        runTraClus(day_to_analyze)
    ####################
    
    #####################################Visualizing##########################################
    
    
    # clusteredTracks = ReadTraclusExport('LOST4Output.txt')
        
        # average_grad_X, average_grad_Y = calculateVector(clusteredTracks)
    
        # #For All Clusters
    # cluster = TrajectoryID_Extraction(clusteredTracks)
    # colors_for_lines = ColorAssignment(clusteredTracks)
    # cluster_line = LinesConstruct(clusteredTracks)
    # Visualizer(cluster_line, colors_for_lines)
    
    #For Separate cluster
    # cluster = TrajectoryID_Extraction(clusteredTracks)
    # colors_for_lines = ColorAssignment(cluster)
    # cluster_line = LinesConstruct(cluster)
    # Visualizer(cluster_line, colors_for_lines)
    
    ##########################################################################################
    
    ######################################### Anomaly Mining ###################################################
    # test_subject = np.array([[200,300],[100,150]])
    counter_new_day = 0
    nj_parameter_array = np.empty([0])
    threshold_array = np.empty([0])
    
    ## nj param
    counter_nj = 0
    while counter_nj < 5:
        filename = "30_days_" + str(counter_new_day + 1) + "_loop_" + str(day_to_analyze) + ".txt"
        # 3-> Thursday
        major_track, end, lines_ori = ReadTraclusExport(filename)
        temp_major_track = major_track
        major_track = major_track[['X', 'Y']]
        major_track = major_track.as_matrix()
        temp_threshold_array = np.empty([0])
#        print(temp_major_track)
        # allFrames 
        tracks = TrajectoryID_Extraction(major_track, allFrames, end, lines_ori)
        # tracks -> all tracks under the cluster
        tracksLine = LinesConstruct(tracks)
        #tracksline -> extract X & Y(a python list)
    #    print(filename)
        nj_param = nj_training_parameter(tracks, temp_major_track)
        nj_parameter_array = np.append(nj_parameter_array, nj_param)
        counter_nj += 1
    nj_param = np.mean(nj_parameter_array)
    probability_array = np.empty([0])
    
    
    # array for second level clustering
    array_second_representative = np.empty([0])
    # threshold calculation
    while counter_new_day < 5:
#        filename = "Day_6_" + str(counter_new_day) + ".txt"
        filename = "30_days_" + str(counter_new_day + 1) + "_loop_" + str(day_to_analyze) + ".txt"
#        filename = "All_days_" + str(day_to_analyze) + ".txt"        
        # 3-> Thursday
        major_track, end, lines_ori = ReadTraclusExport(filename)
        array_second_representative = np.append(array_second_representative, major_track)
        temp_major_track = major_track
        major_track = major_track[['X', 'Y']]
        major_track = major_track.as_matrix()
        temp_threshold_array = np.empty([0])
#        print(temp_major_track)
        # allFrames 
        tracks = TrajectoryID_Extraction(major_track, allFrames, end, lines_ori)
        # tracks -> all tracks under the cluster
        tracksLine = LinesConstruct(tracks)
        #tracksline -> extract X & Y(a python list)
        tracks = tracks[['X', 'Y']]
        tracks = tracks.as_matrix()
        print("similarity")
        threshold_results = calculateSimilarity(temp_major_track, tracks, nj_param)
        temp_threshold_array = np.append(temp_threshold_array, threshold_results)
          
        threshold_array = np.append(threshold_array, min(temp_threshold_array))

        counter_new_day += 1
        
        

    print(threshold_array) 
    threshold_array = np.sort(threshold_array)
    threshold_array = np.percentile(threshold_array, 25)
    file = "threshold_array_" + str(day_to_analyze) + ".txt" 
    output = open(file, 'w')
    output.write(str(threshold_array))
    output.close()
    
    file = "nj_param_" + str(day_to_analyze) + ".txt"
    output = open(file, 'w') 
    output.write(str(nj_param))
    print("threshold array")
    print(threshold_array)
    ############################################################################################################
#    print(allFrames)
TrajectoryClustering_Traclus(True, 3)
#anomaly_detection(True, 6)

#TrajectoryClustering_Traclus(True, 3)