# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 12:34:58 2017

@author: Ice

"""

import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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
    daysToChoose = 365 #30 for original experiment

    # probability calculation
    threshold = np.empty([0])
    
    #####################################################################################################    
    ######### parameters for mon., tues, ..etc. #######   
    os.chdir(root_dir)
    threshold_filename = "threshold_array_" + str(day_to_analyze) + ".txt"    
    output = open(threshold_filename)
    trained_threshold = np.empty([0])
    trained_threshold_temp = output.read().split('\n')
#    trained_threshold = float(trained_threshold)
    trained_threshold_temp = trained_threshold_temp[0:len(trained_threshold_temp)-1] # remove the last empty row      
    for threshold in trained_threshold_temp:
        trained_threshold = np.append(trained_threshold, float(threshold))
    output.close()    
#    print(trained_threshold)
      
    nj_param_file = "nj_param_" + str(day_to_analyze) + ".txt"        
    output = open(nj_param_file)
    nj_param = np.empty([0])
    nj_param_temp = output.read().split('\n')
    nj_param_temp = nj_param_temp[0:len(nj_param_temp)-1] # remove the last empty row          
    for param in nj_param_temp:
        nj_param = np.append(nj_param, float(param))
    output.close()        
#    print(nj_param)
    
    
    date_array = np.empty([0])
    
    ####################################################
    counter = 0
    
    col_names = ['TrackID', 'FrameNo', 'X', 'Y']
#    print(os.getcwd())
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
#                print(date)
        except:
            file_existence_checker += 1
            counter -= 1
            
        # this code is to prevent this while loop from infinite looping
        if file_existence_checker > 366:
            counter = daysToChoose # just terminate the loop is ok ady.        
        counter += 1
    
        currentYear, currentMonth, currentDay, pointerMonth, pointerDay = calendarFunction(currentYear, currentMonth, currentDay, pointerMonth, pointerDay)    
    
#    print(list_day)    
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
#    print(selected_test_dates)
    ##############################################################################
    
    ######## calculate probability and distances ########
    counter = 0
    # reading the representative trajectories
    partition_starts = 0    
    
    probability_array = np.empty([0])
    anomalous = np.empty([0])
    comparative_likelihood = np.empty([0])
    tracker_trained_threshold = 0
    tracker_start = 0

    # plot distance
#    max_distance = np.empty([0])    
    
    while counter < len(selected_test_dates):
        number_of_anomalous_track = 0
        os.chdir(root_dir)     
        filename = "test_day_" + str(counter) + "_" + str(day_to_analyze) + ".txt" 
        representative_traj, end, lines_ori = ReadTraclusExport(filename)
        representative_traj = representative_traj[['TrackID', 'X', 'Y']]
        tracker_trained_threshold = tracker_trained_threshold + representative_traj['TrackID'].max() + 1
        
        # reading test day track
        os.chdir(traj_dir)
        counter_n_parameter = 0  
        currentIndex = 1
        filename = selected_test_dates[counter] + ".txt"
        test_day = pd.read_table(filename, delimiter =' ', header=None, names=col_names)
        test_day = test_day[['TrackID', 'X', 'Y']]
#        print(selected_test_dates[counter])
        probability, number_of_anomalous_track, probability_array, num_track, comparative_likelihood = calculateSimilarity(representative_traj, test_day, nj_param[tracker_start:tracker_trained_threshold], trained_threshold[tracker_start:tracker_trained_threshold], number_of_anomalous_track, comparative_likelihood)
#        probability_array = np.append(probability_array, probability)
        anomalous = np.append(anomalous, number_of_anomalous_track)
#        print(num_track)
        # update start tracker
        tracker_start = tracker_trained_threshold
        
        os.chdir(root_dir)
        
        # plotting distance
#        filename = "distance_" + str(day_to_analyze) + ".txt"
#        if os.path.isfile(filename) == False:
#            output = open(filename, 'w')
#        else:
#            output = open(filename, 'a')
#        for distance in max_distance:
#            output.write(selected_test_dates[counter] + " " + str(distance) + "\n")
#        output.close()        
        
        filename = "anomalous_" + str(day_to_analyze) + ".txt"
        if os.path.isfile(filename) == False:
            output = open(filename, 'w')
        else:
            output = open(filename, 'a')
        output.write(selected_test_dates[counter] + " " + str(number_of_anomalous_track) + "\n")
        
        output.close()
        
        filename = "probability_test_" + str(day_to_analyze) + ".txt"
        if os.path.isfile(filename) == False:
            output = open(filename, 'w')
        else:
            output = open(filename, 'a')
        for probability in probability_array:
            output.write( selected_test_dates[counter] + " "  + str(probability) + "\n")
        output.close()
        
        filename = "total_num_track_" + str(day_to_analyze) + ".txt"
        if os.path.isfile(filename) == False:
            output = open(filename, 'w')
        else:
            output = open(filename, 'a')
        output.write( selected_test_dates[counter] + " "  + str(num_track) + "\n")
        output.close()
        # probability/number of trajectory
#        print("Likelihood of each track")
        
        mean_likelihood_anomalies = sum(probability_array) / num_track
        filename = "likelihood_" + str(day_to_analyze) + ".txt"
        if os.path.isfile(filename) == False:
            output = open(filename, 'w')
        else:
            output = open(filename, 'a')
        output.write( selected_test_dates[counter] + " "  + str(mean_likelihood_anomalies) + "\n")
        output.close()
        
        # likelihood / respective threshold 
#        print("comparative likelihood")
#        print(comparative_likelihood)
#        print("number of trajectories: " + str(num_track))
        mean_comparative = sum(comparative_likelihood) / num_track
#        print(mean_comparative)
        filename = "compare_likelihood_" + str(day_to_analyze) + ".txt"
        if os.path.isfile(filename) == False:
            output = open(filename, 'w')
        else:
            output = open(filename, 'a')
        output.write( selected_test_dates[counter] + " "  + str(mean_comparative) + "\n")
        output.close()
    
    
    
        counter += 1
    ################### plotting anomalous track #######
    os.chdir(img_dir)
#    counter = 0
#    dummy_array = np.empty([0])
#    while counter < len(selected_test_dates):
#        dummy_array = np.append(dummy_array, counter)        
#        counter += 1
    counter = 0
    dummy_array = np.empty([0])

    while counter < len(max_distance):
        dummy_array = np.append(dummy_array, counter)        
        counter += 1

    ###### Each Day Graph #######
    figure_name = "Figure_" + str(day_to_analyze) + ".jpg"
    fig = plt.figure(figsize=(20,20))
    ax = fig.add_subplot(111)
#    plt.xticks(dummy_array, selected_test_dates)
    ax.plot(dummy_array, max_distance)
#    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
    plt.xlabel("Test Dates")
#    plt.ylabel("Number of Anomalies")
    plt.ylabel("distance")
#    fig, ax = plt.plot(dummy_array, anomalous)

    plt.savefig(figure_name)
    plt.show()
    
    ##############################
    


