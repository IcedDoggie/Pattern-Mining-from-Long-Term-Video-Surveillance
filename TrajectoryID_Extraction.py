# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:36:52 2017

@author: Ice
"""

#Decide the color for each cluster
##########stripping the trajectory id#################
def TrajectoryID_Extraction(dataframeInt):
    startTraj_ID = end + 1
    endTraj_ID = len(lines_ori)
    stepTraj_ID = 2
    traj_ID = lines_ori[startTraj_ID:endTraj_ID:stepTraj_ID]
    counter_cluster_ID = 0
    array_for_cluster_ID = []
    count_for_cluster_ID = []
    ## Form ***clusterID***

    while counter_cluster_ID < len(traj_ID):
        count_cluster_ID = 0
        number_of_string = traj_ID[counter_cluster_ID].count(' ')
        while count_cluster_ID < number_of_string:
            array_for_cluster_ID += [counter_cluster_ID]
            count_cluster_ID += 1
        counter_cluster_ID += 1
    array_for_cluster_ID = pd.DataFrame(array_for_cluster_ID)
    
    #sample: elementText = str.replace(elementText, '\\' , '')
    #sample: numpyString = np.fromstring(elementText, dtype=float, sep= ' ' or '\n')
    #sample" dataframeInt = pd.DataFrame(numpyInt)
    ## Stripping string to form ***trajectoryID***
    traj_ID = str(traj_ID)
    traj_ID = str.replace(traj_ID, '[\'', '')
    traj_ID = str.replace(traj_ID, '\']', '')
    traj_ID = str.replace(traj_ID, ', ', '\n')
    traj_ID = str.replace(traj_ID, '\\n', '')
    traj_ID = str.replace(traj_ID, '\'', '')
    traj_ID = np.fromstring(traj_ID, dtype=int, sep=' ')
    traj_ID = pd.DataFrame(traj_ID)
    traj_ID.columns = ['TrackID']
    traj_ID['ClusterID'] = array_for_cluster_ID
    ######################################################

    #check the matched value through joining
#     print(traj_ID)
    tempDF = pd.DataFrame()
    tempDF = pd.merge(concatDay, traj_ID, on='TrackID')
    return tempDF