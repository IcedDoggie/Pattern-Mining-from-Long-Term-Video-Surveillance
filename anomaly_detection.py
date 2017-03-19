# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 12:34:58 2017

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
    daysToChoose = number_of_days #30 for original experiment
    cycle_loop = 8
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
#    day_to_analyze = 1 #0 - monday, 6 - sunday #can prompt for input later
    allFrames = pd.DataFrame() #this is to get back the trajectory for calculating threshold
    
    # probability calculation
    threshold = np.empty([0])
    
    #####################################################################################################    
    threshold_filename = "threshold_array_" + str(day_to_analyze) + ".txt"    
    output = open(threshold_filename)
    trained_threshold = output.read()
    trained_threshold = float(trained_threshold)
#    print(trained_threshold)
    output.close()    
    
#    trained_threshold = trained_threshold.as_matrix()    
    nj_param_file = "nj_param_" + str(day_to_analyze) + ".txt"        
    output = open(nj_param_file)
    nj_param = output.read()
    output.close()        
    
    date_array = np.empty([0])
    nj_param = float(nj_param)

    counter = 0
    
    
    col_names = ['TrackID', 'FrameNo', 'X', 'Y']
    print(os.getcwd())
    counter_file = 0
    currentIndex = 1
    while counter < daysToChoose:
        currentIndex = 1 # This variable is used to reindex every dataframe
        frames = pd.DataFrame()  
        os.chdir(traj_dir)
        stringDate = '001_' + str(currentYear) + str(currentMonth) + str(currentDay) + '.txt' 
        date = str(currentYear) + str(currentMonth) + str(currentDay)
        string_to_be_parsed = "pd.read_table('" + stringDate + "',delimiter=' ', header=None, names=col_names)"     
        datetime_convert = datetime.strptime(date, '%Y%m%d')
        dayInWeek = datetime_convert.weekday()
        try:
            exec("%s%d = %s" % ("day", counter, string_to_be_parsed))
            tempString_Date = eval("%s%d" % ("day", counter)) 
            tempString_Date, currentIndex = trackID_reindex(tempString_Date, currentIndex)
            if dayInWeek == day_to_analyze:
                frames = frames.append(tempString_Date)
                date_array = np.append(date_array, str(date))
                print(str(date))
        except:
            counter -= 1
            
        counter += 1

        currentYear, currentMonth, currentDay, pointerMonth, pointerDay = calendarFunction(currentYear, currentMonth, currentDay, pointerMonth, pointerDay)
    #     #######################################################################################
        os.chdir(root_dir)        
        if len(frames) > 0:        
            concatDay = frames.sort_values(by='TrackID', ascending=True)
            allFrames = allFrames.append(concatDay)
            concatDay = concatDay.reset_index(drop=True)
            if traFileCreation == True and dayInWeek == day_to_analyze:    
                counter_file += 1
    
    
 
    
    ##################################
    
    counter = 0
    threshold_mining = np.empty([0])
    anomaly_trigger = np.empty([0])
    ### Choose representative file with most representative tracks
    # instead of choosing highest track count, we can concatenate
    # all representative track
    # concatenate is not a good idea imo, i should choose based on respective
    # months
    highest_track_count = 0
    while counter < cycle_loop:
        filename_representative = "30_days_" + str(counter + 1) + "_loop_" + str(day_to_analyze) + ".txt"
        representative_track_temp, end2, lines_ori2 = ReadTraclusExport(filename_representative)        
        representative_track_temp = LinesConstruct(representative_track_temp)
        if len(representative_track_temp) > highest_track_count:
            highest_track_count = counter + 1
        counter += 1        
    counter = 0

    
    emptytracks = False

    # Select respective representative trajectory based on which-30-days
    count = 1
    periodic_count = number_of_days / 30 #periodic count is to select the file
    while count <= periodic_count:
        filename_representative = "30_days_" + str(count) + "_loop_" + str(day_to_analyze) + ".txt"    
        os.chdir(traj_dir)
        try:
            new_track = concatDay[['TrackID', 'X', 'Y']]
        except:
            emptytracks = True
        if emptytracks == False:
            os.chdir(root_dir)
            representative_track, end2, lines_ori2 = ReadTraclusExport(filename_representative)               
            cluster_line = LinesConstruct(new_track)
            threshold_results = calculateSimilarity(representative_track, cluster_line, nj_param)        
            counter += 1
            print("threshold results")
            print(threshold_results) 
            threshold_mining = np.append(threshold_mining, threshold_results)
            
            if threshold_results[0] < trained_threshold:
                anomaly_trigger = np.append(anomaly_trigger, 1)
            else:
                anomaly_trigger = np.append(anomaly_trigger, 0)
            
        count += 1
    # indicate whether that day is abnormal or normal
    counter = 0
    file = "threshold_mining_" + str(day_to_analyze) + ".txt"
    output = open(file, 'w')    
    while counter < len(threshold_mining):
        anomaly_trigger[counter] = int(anomaly_trigger[counter])
        output.write(str(threshold_mining[counter]) + " " + date_array[counter] + " " + str(anomaly_trigger[counter]) + "\n")
        counter += 1
    output.close()