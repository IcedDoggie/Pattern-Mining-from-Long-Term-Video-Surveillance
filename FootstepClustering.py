# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:38:56 2017

@author: Ice
"""

###### import pandas as pd
import numpy as np
import cv2
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster import hierarchy
import sklearn
from pandas import Series, DataFrame, Panel
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import matplotlib.image as mpimg
from matplotlib import collections as mc 
import os
import matplotlib.ticker as ticker
import collections

import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO

##################################### Tunable Variables ###########################################
days_to_process = 7
pd.options.display.max_rows = 10
###################################################################################################

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
daysToChoose = 235 # currently hardcoded, 235 is for entire year of 2012
#####################################################################################################

############# Calling functions #############
agglomerativeClustering_Code = open('agglomerativeClustering.py').read()
fancydendrogram_Code = open('fancy_dendrogram.py').read()
heatmapPool_Code = open('heatmapPooling.py').read()
histogram_Code = open('histogram.py').read()
heatmap_Code = open('heatmapConstruction.py').read()
trackID_Code = open('trackID_reindex.py').read()
calendar_Code = open('calendarFunction.py').read()

exec(agglomerativeClustering_Code)
exec(fancydendrogram_Code)
exec(heatmapPool_Code)
exec(histogram_Code)
exec(heatmap_Code)
exec(trackID_Code)
exec(calendar_Code)
#############################################


###############################string concatenation & Load Data########################
counter = 0
frames = pd.DataFrame()
# os.chdir('E:\Documents\MMU Studies\Python Scripts\Track Blobs')
os.chdir('E:\Documents\MMU Studies\Python Scripts\Track LOST dataset')
currentIndex = 1 # This variable is used to reindex every dataframe
print(os.getcwd())
listDay = []
# list season is a list for specifying spring, summer or winter in the visualization
listSeason = []
listDate = []
listDate += [0]
listDate_for_topbottom = []
listDate_for_topbottom += [0]
while counter < daysToChoose:
    stringDate = '001_' + str(currentYear) + str(currentMonth) + str(currentDay) + '.txt' 
    string_to_be_parsed = "pd.read_table('" + stringDate + "',delimiter=' ', header=None, names=col_names)"
    try:
        exec("%s%d = %s" % ("day", counter, string_to_be_parsed))
        tempString_Date = eval("%s%d" % ("day", counter))
        tempString_Date, currentIndex = trackID_reindex(tempString_Date, currentIndex)
        tempList = tempString_Date[['X', 'Y']]
        frames = frames.append(tempString_Date)
        tempFrames = frames[['X', 'Y']]
        listDay += [tempList]
        listSeason += [currentMonth]
        date = str(currentYear) + str(currentMonth) + str(currentDay)
        if counter%6==0:
            listDate += [date]
        if counter%20 == 0:
            listDate_for_topbottom += [date]
        print("Found")
    except:
        print("Not Found")
        counter -= 1
    
    counter += 1
    currentYear, currentMonth, currentDay, pointerMonth, pointerDay = calendarFunction(currentYear, currentMonth, currentDay, pointerMonth, pointerDay)
#######################################################################################
col_names = ['TrackID','FrameNo', 'X', 'Y']
concatDay = frames.sort_values(by='TrackID', ascending=True)
concatDay = concatDay.reset_index(drop=True)
os.chdir('E:\Documents\MMU Studies\Python Scripts')
# np.set_printoptions(threshold=np.nan)
# heatmap_data = constructHeatmap(concatDay)


counter = 0
axis_counter = 0
np_vector_heatmap = []
np_mat = []
np_mat2 = []
np_mat_topbottom = np.empty((48,0)) # 48 is the total number of pools

while counter < daysToChoose:
    heatmap_data = constructHeatmap(listDay[counter])
    vector_heatmap, sum_array, sum_array_top_bottom = heatmapPooling(heatmap_data, 80)
    np_mat += [sum_array]
    np_mat2 += [sum_array_top_bottom]
    np_mat_topbottom = np.insert(np_mat_topbottom, 0, sum_array_top_bottom, axis = 1)
    np_vector_heatmap += [vector_heatmap]
    counter += 1
    axis_counter += 1

np_vector_heatmap = np.asarray(np_vector_heatmap)
# np_mat_transpose = list(map(list, zip(*np_mat))) #cannot transpose cuz it only changes the sides
# print(np_mat_transpose)
# print(max(np_mat[0]))
# print(min(np_mat[0]))
clustered_data = agglomerativeClustering(heatmap_data, np_mat)

# test_transpose_of_topbottom = np_mat_topbottom.transpose()

#2012-1-1 -> 2013-5-18
# print(listDate)
### showing heatmap
# print(listSeason)
# counter_season = 0
# seasons = []
# while counter_season < len(listSeason):
# #     if counter_season % 10 == 0:
#     if listSeason[counter_season] == "12" or listSeason[counter_season] == "01" or listSeason[counter_season] == "02":
#         seasons += ['winter']
#     elif listSeason[counter_season] == "03" or listSeason[counter_season] == "04" or listSeason[counter_season] == "05":
#         seasons += ['spring']
#     elif listSeason[counter_season] == "06" or listSeason[counter_season] == "07" or listSeason[counter_season] == "08":
#         seasons += ['summer']   
#     else:
#         seasons += ['autumn']
#     counter_season += 1


# fig = plt.figure(figsize=(20,20))
# # fig = plt.figure()
# ax = fig.add_subplot(111)
# # heatmap_vector = ax.matshow(np_mat)
# ax.matshow(np_mat)

######################################### Feature vector Visualization ####################################################
# fig2 = plt.figure(figsize=(20,20))
# ax2 = fig2.add_subplot(111)
# ax2.matshow(np_mat)
# # ax2.matshow(np_mat_topbottom_transpose)
# ax2.set_yticklabels(listDate)
# ax2.yaxis.set_major_locator(ticker.MultipleLocator(6))
# # plt.savefig('Heatmap_VEC_2012_with_date.png')

# fig3 = plt.figure(figsize=(20,20))
# ax3 = fig3.add_subplot(111)
# ax3.matshow(np_mat_topbottom)
# # ax3.matshow(np_mat2)
# # ax3.matshow(np_mat)
# ax3.set_xticklabels(listDate_for_topbottom)
# ax3.xaxis.set_major_locator(ticker.MultipleLocator(20))
# # plt.savefig('Heatmap_VEC_2012_with_date_top_bottom.png')
###########################################################################################################################

# plt.show()