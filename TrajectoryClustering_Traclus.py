# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 15:02:07 2017

@author: Ice
"""

import pandas as pd
import numpy as np
import os
import os.path
import sys
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
def TrajectoryClustering_Traclus(traFileCreation, day_to_analyze, year_to_analyze, root_dir, traj_dir, img_dir):
    #####################################string variables##############################################
    dayArray = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17'
    ,'18','19','20','21','22','23','24','25','26','27','28','29','30','31']
    monthArray = ['01','02','03','04','05','06','07','08','09','10','11','12',]
    # Tunable Variables
    # currentYear = 2013 # input 1
    # pointerMonth = n n1	   # input 2
    # pointerDay = 0   # input 3
    
    currentYear = year_to_analyze
    currentMonth = monthArray[0]
    currentDay = dayArray[0]
    pointerMonth = 0
    pointerDay = 0
    daysToChoose = 60 #30 for original experiment
    cycle_loop = 8
    cycle_counter = 0
    num_days = 4 # this parameter sets total days to be considered
    n_parameter = 3 # this parameter sets how many previous training days
    annotate_testdays = np.empty([0]) 
    list_day = np.empty([0])
    vid_num = '001'
    
#    day_to_analyze = 2 #0 - monday, 6 - sunday #can prompt for input later
    allFrames = pd.DataFrame() #this is to get back the trajectory for calculating threshold
    
    # probability calculation
    threshold = np.empty([0])
    
    #####################################################################################################    
    currentIndex = 1 # This variable is used to reindex every dataframe
    
    #################### create an array of dates with the respective day(eg: monday) ###################
    n_param_counter = n_parameter
    num_days_counter = 0   
    counter = 0
    file_existence_checker = 0
    frames = pd.DataFrame()
    while counter < daysToChoose:
        os.chdir(traj_dir)          
        date = str(currentYear) + str(currentMonth) + str(currentDay)
        stringDate = vid_num + "_" + str(currentYear) + str(currentMonth) + str(currentDay)
        filename_for_test_existence = stringDate + ".txt"        
        datetime_convert = datetime.strptime(date, '%Y%m%d')
        dayInWeek = datetime_convert.weekday()
        try:          
            exist = os.path.isfile(filename_for_test_existence)
            if dayInWeek == day_to_analyze and exist == True:
                n_param_counter -= 1  
                num_days_counter += 1
                list_day = np.append(list_day, stringDate)
                print(date)
        except:
            file_existence_checker += 1
            counter -= 1
            
        # this code is to prevent this while loop from infinite looping
        if file_existence_checker > 366:
            counter = daysToChoose # just terminate the loop is ok ady.        
        counter += 1
    
        currentYear, currentMonth, currentDay, pointerMonth, pointerDay = calendarFunction(currentYear, currentMonth, currentDay, pointerMonth, pointerDay)    
    #####################################################################################################
    print(list_day)
    print(len(list_day))
    print("start tra")
#    os.chdir(root_dir)
    ########################### Make up and create TRA File ##################    
    counter_list_day = 0
    days_in_partition = 0
    frames = pd.DataFrame()
    date_verifier = []
    partition_num = 0
    start_partition = 0 # just a initial value helping partition num
    col_names = ['TrackID', 'FrameNo', 'X', 'Y']
    while counter_list_day < ( len(list_day) - n_parameter ):   
        while days_in_partition < n_parameter:
            filename = list_day[partition_num] + '.txt'
            date_verifier += [filename]
            string_to_be_parsed = "pd.read_table('" + filename + "',delimiter=' ', header=None, names=col_names)"                    
            exec("%s%d = %s" % ("day", counter_list_day, string_to_be_parsed))                 
            tempString_Date = eval("%s%d" % ("day", counter_list_day))   
            tempString_Date, currentIndex = trackID_reindex(tempString_Date, currentIndex)
            frames = frames.append(tempString_Date)
            partition_num += 1
            days_in_partition += 1
        if days_in_partition == n_parameter and traFileCreation == True:
            if len(frames) > 0:
                concatDay = frames.sort_values(by='TrackID', ascending=True)
                allFrames = allFrames.append(concatDay)
                concatDay = concatDay.reset_index(drop=True)
            filename = "test_day_" + str(counter_list_day) + "_" + str(day_to_analyze) + ".tra"
            os.chdir(root_dir)            
            TraClusFileExporter(concatDay, filename)            
            runTraClus(day_to_analyze, counter_list_day)   
            start_partition += 1
            partition_num = start_partition
            days_in_partition = 0
            frames = pd.DataFrame()
            os.chdir(traj_dir)
        else:
            days_in_partition = 0            
        counter_list_day += 1
#    print(date_verifier) # verifying the dates trained sequentially

    ####################################Visualizing Multiple##########################################
#    print(annotate_testdays)
    visualize_num = 5
    visualize_count = 0
    inner_loop_count = 0


    counter_new_day = 0
    nj_parameter_array = np.empty([0])
    threshold_array = np.empty([0])
    
    ## nj param
    os.chdir(root_dir)
    counter_nj = 0
    while counter_nj < ( len(list_day) - n_parameter ):
        
        filename = "test_day_" + str(counter_nj) + "_" + str(day_to_analyze) + '.txt'
        image_filename = "test_day_" + str(counter_nj) + "_" + str(day_to_analyze) + '.jpg'
         
        # 3-> Thursday
        major_track, end, lines_ori = ReadTraclusExport(filename)
        temp_major_track = major_track
        major_track = major_track[['X', 'Y']]
        major_track = major_track.as_matrix()
        temp_threshold_array = np.empty([0])
        
#        cluster = TrajectoryID_Extraction(temp_major_track, temp_major_track, end, lines_ori)
            
        colors_for_lines = ColorAssignment(temp_major_track)
        cluster_line = LinesConstruct(temp_major_track)
        Visualizer(cluster_line, colors_for_lines, image_filename, root_dir, img_dir)     
        
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
    while counter_new_day < ( len(list_day) - n_parameter ):
#        filename = "Day_6_" + str(counter_new_day) + ".txt"
        filename = "test_day_" + str(counter_new_day) + "_" + str(day_to_analyze) + '.txt'
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
#        tracks = tracks[['X', 'Y']]
#        tracks = tracks.as_matrix()
#        print("similarity")
        threshold_results = calculateSimilarity(temp_major_track, tracksLine, nj_param)
        temp_threshold_array = np.append(temp_threshold_array, threshold_results)
          
        threshold_array = np.append(threshold_array, min(temp_threshold_array))

        counter_new_day += 1
        
        

#    print(threshold_array) 
    threshold_array = np.sort(threshold_array)
    threshold_array = np.percentile(threshold_array, 50)
    file = "threshold_array_" + str(day_to_analyze) + ".txt" 
    output = open(file, 'w')
    output.write(str(threshold_array))
    output.close()
    
    file = "nj_param_" + str(day_to_analyze) + ".txt"
    output = open(file, 'w') 
    output.write(str(nj_param))
#    print("threshold array")
#    print(threshold_array)
    ############################################################################################################
#    print(allFrames)
#userParam = sys.argv
#export_file = bool(userParam[1])
#day_in_week = int(userParam[2])
#year = int(userParam[3])
#num_days = int(userParam[4])
#root_dir = str(userParam[5])
#data_dir = str(userParam[6])
#image_dir = str(userParam[7])
#
#print(type(export_file))
#able_to_run = 0
#try:
#    
#    if type(export_file) != type(True):
#        print("Invalid datatype. First param must be boolean")
#    else:
#        able_to_run += 1
#    if type(day_in_week) != type(1):
#        print("Invalid datatype. Second param must be int")
#    else:
#        able_to_run += 1
#    if able_to_run == 2:
#        TrajectoryClustering_Traclus(export_file, day_in_week, year, root_dir, data_dir, image_dir)
#                
#        anomaly_detection(export_file, day_in_week, num_days, year, root_dir, data_dir, image_dir)
#except:
#    print("Invalid Input. Make sure it's TrajectoryClustering_Traclus.py [bool(True|False)] [int(0~6)]")
TrajectoryClustering_Traclus(True, 0, 2012, 'E:\Documents\MMU Studies\Python Scripts', 'E:\Documents\MMU Studies\Python Scripts\Track LOST dataset', "E:\Documents\MMU Studies\Python Scripts\Trajectories")
#TrajectoryClustering_Traclus(True, 1, 2012, 'E:\Documents\MMU Studies\Python Scripts', 'E:\Documents\MMU Studies\Python Scripts\Track LOST dataset', "E:\Documents\MMU Studies\Python Scripts\Trajectories")
#TrajectoryClustering_Traclus(True, 2, 2012, 'E:\Documents\MMU Studies\Python Scripts', 'E:\Documents\MMU Studies\Python Scripts\Track LOST dataset', "E:\Documents\MMU Studies\Python Scripts\Trajectories")
#TrajectoryClustering_Traclus(True, 3, 2012, 'E:\Documents\MMU Studies\Python Scripts', 'E:\Documents\MMU Studies\Python Scripts\Track LOST dataset', "E:\Documents\MMU Studies\Python Scripts\Trajectories")
#TrajectoryClustering_Traclus(True, 4, 2012, 'E:\Documents\MMU Studies\Python Scripts', 'E:\Documents\MMU Studies\Python Scripts\Track LOST dataset', "E:\Documents\MMU Studies\Python Scripts\Trajectories")
#TrajectoryClustering_Traclus(True, 5, 2012, 'E:\Documents\MMU Studies\Python Scripts', 'E:\Documents\MMU Studies\Python Scripts\Track LOST dataset', "E:\Documents\MMU Studies\Python Scripts\Trajectories")
#TrajectoryClustering_Traclus(True, 6, 2012, 'E:\Documents\MMU Studies\Python Scripts', 'E:\Documents\MMU Studies\Python Scripts\Track LOST dataset', "E:\Documents\MMU Studies\Python Scripts\Trajectories")
#anomaly_detection(True, 0, 60, 2012, 'E:\Documents\MMU Studies\Python Scripts', 'E:\Documents\MMU Studies\Python Scripts\Track LOST dataset', "E:\Documents\MMU Studies\Python Scripts\Trajectories")


#TrajectoryClustering_Traclus(True, 0, 2012)
#anomaly_detection(True, 0, 2012, 'E:\Documents\MMU Studies\Python Scripts\Track LOST dataset', 'E:\Documents\MMU Studies\Python Scripts', "E:\Documents\MMU Studies\Python Scripts\Trajectories")
    
#anomaly_detection(True, 0, 192, 2012,  'E:\Documents\MMU Studies\Python Scripts\Track LOST dataset', 'E:\Documents\MMU Studies\Python Scripts', "E:\Documents\MMU Studies\Python Scripts\Trajectories")
#TrajectoryClustering_Traclus(True, 1, 2012)
#anomaly_detection(True, 1, 192, 2012)
#TrajectoryClustering_Traclus(True, 2, 2012)
#anomaly_detection(True, 2, 192, 2012)
#TrajectoryClustering_Traclus(True, 3, 2012)
#anomaly_detection(True, 3, 192, 2012)
#TrajectoryClustering_Traclus(True, 4, 2012)
#anomaly_detection(True, 4, 192, 2012)
#TrajectoryClustering_Traclus(True, 5, 2012)
#anomaly_detection(True, 5, 192, 2012)
#TrajectoryClustering_Traclus(True, 6, 2012)
#anomaly_detection(True, 6, 192, 2012)

#anomaly_detection(True, 6)

#TrajectoryClustering_Traclus(True, 3)