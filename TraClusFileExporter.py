# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:38:20 2017

@author: Ice
"""
import numpy as np

# Prepare .tra extension file for TraClus clustering algorithm
def TraClusFileExporter(concatDay, filename):
    outputFile = []
    concatDay = concatDay[['TrackID', 'X', 'Y']]
    concatDayWithoutID = concatDay[['X', 'Y']]
    concatDayWithID = concatDay[['TrackID']]
    concatDayWithID = concatDayWithID.drop_duplicates('TrackID')
    concatDayWithID = concatDayWithID.values  #it's an array now


    # slicing the dataframe based on ID
    row_iterator = concatDay.iterrows()
    row_id, this_row = next(row_iterator)
    #slicing dataframe to respective arrays for LineCollection function
    initialID = this_row['TrackID']
    slicingArray = []

    ####################suspected bug################################
    for i, rows in row_iterator:
        if rows['TrackID'] != initialID:
            slicingArray.append(i)
            initialID = rows['TrackID']

    newList = np.split( concatDayWithoutID, slicingArray )

    ####################suspected bug################################

    #Now: We need to combine every single piece of data to conform with .tra
    #header: number of dimensions
    #      : number of trajectories
    number_of_dimension = 2
    number_of_trajectory = len(concatDayWithID)
    arrayForHeader = str(number_of_dimension) + '\n' + str(number_of_trajectory) + '\n'
#     print(concatDayWithID)
    #format: TrackID no_trajectory_point X1 Y1 X2 Y2... Xn Yn
    arrayForXY = []
    number_of_ID = len(concatDayWithID)
    counter_for_points = 0
    counter_for_ID = 0

    while counter_for_ID < number_of_ID:
        # reset
        counter_for_points = 0
        # Convert ID to proper string form
        tempID = concatDayWithID[counter_for_ID]
        number_of_trajectory_points = len(newList[counter_for_ID])
        stringForTempID = str(tempID)
        stringForTempID = stringForTempID[1:-1]
        # concatenation
        if len(arrayForXY) == 0:
            arrayForXY = stringForTempID + ' ' + str(number_of_trajectory_points) + ' '
        else:
            arrayForXY += stringForTempID + ' ' + str(number_of_trajectory_points) + ' '
        while counter_for_points < number_of_trajectory_points:  
            # Select X and Y
            tempHelper = newList[counter_for_ID]
            tempArray = tempHelper.iloc[counter_for_points]
            helperX = tempArray[0]
            helperY = tempArray[1]
            arrayForXY += str(helperX) + ' ' + str(helperY) + ' '
            counter_for_points += 1
            if counter_for_points == number_of_trajectory_points:
                arrayForXY += '\n'
        counter_for_ID += 1

    finalOutput = arrayForHeader + arrayForXY    

    output = open(filename, 'w')
    output.write(finalOutput)
    output.close()