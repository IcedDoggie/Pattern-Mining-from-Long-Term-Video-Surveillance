# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:36:29 2017

@author: Ice
"""
import pandas as pd
import numpy as np

# Get the output from TraClus, revamp and prepare data to visualize
# to achieve this, i need to read from text file and reconstruct it back to a dataframe.
def ReadTraclusExport(filename):
    fileOpener = open(filename, 'r')
    lines_ori = fileOpener.readlines()

    ########Choose the rows with X Y coordinates####################################
    #a loop is needed to differentiate the xy and affilitated trajectory's id
    counterLineNumber = 0 
    for lines in lines_ori:
        indexOfTraj = lines.find("trajectoryID: 0")
        if indexOfTraj == 0:
            break
        counterLineNumber += 1

    start = 2
    end = counterLineNumber 
    step = 2
    lines = lines_ori[start:end:step]
    ################################################################################

    ####################Choose the rows with ID and number of points################
    clusterID_array = []
    num_points = []
    start = 1
    end = counterLineNumber
    step = 2
    lines_ID = lines_ori[start:end:step]
    length_lines_ID = len(lines_ID)
    counter_for_linesID = 0
    
    #a global list for accessment
    global end, lines_ori
    
    while counter_for_linesID < length_lines_ID:
        temp_lines_ID = str(lines_ID[counter_for_linesID])
        temp_index = temp_lines_ID.find(" ")
        temp_index3 = temp_lines_ID.find("P")
        temp_index2 = temp_lines_ID.find("  ", 14, len(temp_lines_ID))
        clusterID_array += [temp_lines_ID[temp_index + 1:temp_index3]]
        num_points += [temp_lines_ID[temp_index2 + 2:]]
        counter_for_linesID += 1
    ##################################################################################

    #Strip the string into appropriate form
    element = str(lines)
    elementText = element[0:-1]
    elementText = str.replace(elementText, '\\' , '')
    elementText = str.replace(elementText, "n", '')
    elementText = str.replace(elementText, "   ", " ")
    elementText = str.replace(elementText, ",", "\n")
    elementText = str.replace(elementText, "\n", '')
    elementText = str.replace(elementText, "'", "" )
    elementText = str.replace(elementText, "  "," ")
    elementText = str.replace(elementText, "[", "")

    #put in 2d array form and convert to integer
    numpyString = np.fromstring(elementText, dtype=float, sep= ' ' or '\n')
    numpyInt = numpyString.astype(int)
    number_of_rows = int( len(numpyInt)/2 )
    numpyInt = numpyInt.reshape((number_of_rows,2))

    #convert numpy array to dataframe
    dataframeInt = pd.DataFrame(numpyInt)
    dataframeInt.columns = ['X', 'Y']
    dataframeInt = dataframeInt.convert_objects(convert_numeric=True)

    #Assign ID to specific tracks
    temp_array_ID = []
    total_num_points = len(num_points)
    counter_for_total_num = 0
    while counter_for_total_num < total_num_points:
        tempCounter_for_num = 0
        while tempCounter_for_num < int(num_points[counter_for_total_num]):
            temp_array_ID += [clusterID_array[counter_for_total_num]]
            tempCounter_for_num += 1
        counter_for_total_num += 1

    #finalized output
    temp_array_ID = list(map(int, temp_array_ID))
    dataframeInt['TrackID'] = temp_array_ID
    cols = dataframeInt.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    dataframeInt = dataframeInt[cols]

    return dataframeInt, end, lines_ori