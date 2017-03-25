# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 12:34:58 2017

@author: Ice

"""

import pandas as pd
import numpy as np
import os
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
from runTraClus_singleDay import runTraClus_singleDay
#from TrajectoryClustering_Traclus import TrajectoryClustering_Traclus


import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

def anomaly_detection(traFileCreation, day_to_analyze, number_of_days, year_to_analyze, root_dir, traj_dir, img_dir):
##################################### Tunable Variables ###########################################
# days_to_process = 7
    pd.options.display.max_rows = 100
###################################################################################################
    
    #####################################string variables##############################################
    dayArray = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17'
    ,'18','19','20','21','22','23','24','25','26','27','28','29','30','31']
    monthArray = ['01','02','03','04','05','06','07','08','09','10','11','12']
    # Tunable Variables
    # currentYear = 2013 # input 1
    # pointerMonth = n n1	   # input 2
    # pointerDay = 0   # input 3
    # date until 20120610 <- training set
    # 20120611 - 20121230 <- test set
    currentYear = year_to_analyze
    currentMonth = monthArray[0]
    currentDay = dayArray[0]
    pointerMonth = 0
    pointerDay = 0
    daysToChoose = 60 #30 for original experiment

    # probability calculation
    threshold = np.empty([0])
    
    #####################################################################################################    
    ######### parameters for mon., tues, ..etc. #######    
    threshold_filename = "threshold_array_" + str(day_to_analyze) + ".txt"    
    output = open(threshold_filename)
    trained_threshold = output.read()
    trained_threshold = float(trained_threshold)
    output.close()    
      
    nj_param_file = "nj_param_" + str(day_to_analyze) + ".txt"        
    output = open(nj_param_file)
    nj_param = output.read()
    output.close()        
    date_array = np.empty([0])
    nj_param = float(nj_param)
    ####################################################
    counter = 0
    
    col_names = ['TrackID', 'FrameNo', 'X', 'Y']
    print(os.getcwd())
    counter_file = 0
    currentIndex = 1
    n_parameter = 3 # this parameter sets how many previous training days
    vid_num = '001'
    list_day = np.empty([0])
    #################### create an array of dates with the respective day(eg: monday) ###################
    n_param_counter = n_parameter
    num_days_counter = 0   
    counter = 0
    file_existence_checker = 0
    
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
    
    print(list_day)    
    test_dates_array = np.empty([0])
    ########################## load the test dates ###############################
    os.chdir(root_dir)    
    filename = "test_days_list_" + str(day_to_analyze) + ".txt"    
    output = open(filename, 'r')
    test_dates = output.read().split('\n')
    output.close()
    test_dates = test_dates[0:len(test_dates)-1] # remove the last empty row   

    
    ######## filter test dates that are in range of daysToChoose ########
    selected_test_dates = np.empty([0])
    for dates in test_dates:
        if dates <= list_day[len(list_day)-1]:
            selected_test_dates = np.append(selected_test_dates, dates)
    print(selected_test_dates)
    ##############################################################################
    
    ######## calculate probability and distances ########
    counter = 0
    # reading the representative trajectories
    partition_starts = 0    
    
    while counter < len(selected_test_dates):
        os.chdir(root_dir)
        partition_num = partition_starts
        n_param_frames = pd.DataFrame()      
        filename = "test_day_" + str(counter) + "_" + str(day_to_analyze) + ".txt" 
        representative_traj, end, lines_ori = ReadTraclusExport(filename)
        representative_traj = representative_traj[['X', 'Y']]
        representative_traj = representative_traj.as_matrix()        
#        print(representative_traj)
        print(filename)
        
        # reading each day track
        os.chdir(traj_dir)
        counter_n_parameter = 0    
        while counter_n_parameter < n_parameter:
            filename = list_day[partition_num] + ".txt"
            n_param_frames = n_param_frames.append( pd.read_table(filename, delimiter = " ", header=None, names=col_names) )
            counter_n_parameter += 1
            partition_num += 1
            print(filename)
        counter += 1       
#        print(n_param_frames)
        partition_starts += 1
    #####################################################
    counter = 0
    threshold_mining = np.empty([0])
    anomaly_trigger = np.empty([0])

    # indicate whether that day is abnormal or normal
    counter = 0
    file = "threshold_mining_" + str(day_to_analyze) + ".txt"
    output = open(file, 'w')    
    while counter < len(threshold_mining):
        anomaly_trigger[counter] = int(anomaly_trigger[counter])
        output.write(str(threshold_mining[counter]) + " " + date_array[counter] + " " + str(anomaly_trigger[counter]) + "\n")
        counter += 1
    output.close()