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


import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

##################################### Tunable Variables ###########################################
# days_to_process = 7
pd.options.display.max_rows = 100
###################################################################################################


#### Calling all functions #####
#direction_Code = open('DirectionCalculation.py').read()
#calendar_Code = open('calendarFunction.py').read()
#chamferDistance_Code = open('chamfer_distance.py').read()
#colorAssignment_Code = open('ColorAssignment.py').read()
#linesConstruct_Code = open('LinesConstruct.py').read()
#nj_training_Code = open('nj_training_parameter.py').read()
#readTraclusExport_Code = open('ReadTraclusExport.py').read()
#reindex_Code = open('trackID_reindex.py').read()
#traclusExport_Code = open('TraClusFileExporter.py').read()
#pivoting_Code = open('trajectory_pivoting_based_on_id.py').read()
#trajectoryID_Code = open('TrajectoryID_Extraction.py').read()
#similarity_Code = open('calculateSimilarity.py').read()
#visualizer_Code = open('Visualizer.py').read()
##
#exec(direction_Code)
#exec(calendar_Code)
#exec(chamferDistance_Code)
#exec(colorAssignment_Code)
#exec(linesConstruct_Code)
#exec(nj_training_Code)
#exec(readTraclusExport_Code)
#exec(reindex_Code)
#exec(traclusExport_Code)
#exec(pivoting_Code)
#exec(trajectoryID_Code)
#exec(similarity_Code)
#exec(visualizer_Code)

    ###############################string concatenation & Load Data########################
def TrajectoryClustering_Traclus(traFileCreation):
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
    day_to_analyze = 3 #0 - monday, 6 - sunday #can prompt for input later
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
    
    #################### Visualizing first hierarchy ######################
    #while inner_loop_count <= 6:
    #     concat_df = pd.DataFrame()
    #     visualize_count = 0
    #     currentIndex = 1
    #     while visualize_count < visualize_num:
    #         visualize_count += 1
    ##         filename = '30_days_' + str(visualize_count) + "_loop_" + str(inner_loop_count)
    #         filename = str(inner_loop_count) + "_cluster" 
    #         filename_extension = filename + ".txt"
    #        
    #         clusteredTracks = ReadTraclusExport(filename_extension)
    #         tempString_Date, currentIndex = trackID_reindex(clusteredTracks, currentIndex)
    #         concat_df = concat_df.append(tempString_Date)
    #         cluster = TrajectoryID_Extraction(clusteredTracks)
    #         colors_for_lines = ColorAssignment(clusteredTracks)
    #         cluster_line = LinesConstruct(clusteredTracks)
    ##         Visualizer(cluster_line, colors_for_lines, filename)
    #    
    #    print(cluster)
    ##     filename = str(inner_loop_count) + "_cluster.tra"  
    ##     concat_df = concat_df.sort_values(by='TrackID', ascending=True)
    ##     concat_df = concat_df.reset_index(drop=True)    
    ##     TraClusFileExporter(concat_df, filename)    
    #     inner_loop_count += 1
    ########################################################################
    
    #################### Visualizing second hierarchy ######################
    current_day_to_be_analyzed = 0
    day_counter = 0
    while day_counter <= 6:
        filename = str(day_counter) + "_cluster" 
        filename_extension = filename + ".txt"
        
        clusteredTracks, end, lines_ori = ReadTraclusExport(filename_extension)
        if current_day_to_be_analyzed == day_counter:
            current_day_representative_track = clusteredTracks        # this line get the representative track for particular day
            nj_parameter = nj_training_parameter( concatDay, current_day_representative_track )
    #        print("nj param: " + str(nj_parameter))
        cluster = TrajectoryID_Extraction(clusteredTracks, allFrames, end, lines_ori)
        colors_for_lines = ColorAssignment(clusteredTracks)
        cluster_line = LinesConstruct(clusteredTracks)
        
    #     Visualizer(cluster_line, colors_for_lines, filename)
    #     print(clusteredTracks)
        day_counter += 1
    
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
    threshold = 0.03
    # test_subject = np.array([[200,300],[100,150]])
    counter_new_day = 0

    while counter_new_day < 5:
#        filename = "Day_6_" + str(counter_new_day) + ".txt"
        filename = "30_days_" + str(counter_new_day + 1) + "_loop_3" + ".txt"
        major_track, end, lines_ori = ReadTraclusExport(filename)
        major_track = major_track[['X', 'Y']]
        major_track = major_track.as_matrix()
        
        tracks = TrajectoryID_Extraction(major_track, allFrames, end, lines_ori)
        tracksLine = LinesConstruct(tracks)
    #    print(filename)
    #    print(major_track)
        for each in tracksLine:
            each = each.as_matrix()
            threshold_calculation(major_track, each)

        probability = calculateSimilarity(current_day_representative_track, major_track, nj_parameter)
    #    print( "Probability: " + str(probability))
        counter_new_day += 1
    
    # print((clusteredTracks))
    
    # nj_parameter = nj_training_parameter( concatDay, clusteredTracks)
    # probability = calculateSimilarity(clusteredTracks, test_subject, nj_parameter)
    # print(probability)
    ############################################################################################################
#    print(allFrames)
TrajectoryClustering_Traclus(False)