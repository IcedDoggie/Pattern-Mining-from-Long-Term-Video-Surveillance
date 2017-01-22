# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:35:42 2017

@author: Ice
"""

def calculateGradient(dataframeInput):
    tempnp = pd.DataFrame.as_matrix(dataframeInput[['X']])
    tempnp = tempnp.ravel()
    dataframe_gradient_X = np.gradient(tempnp)
    
    tempnp = pd.DataFrame.as_matrix(dataframeInput[['Y']])
    tempnp = tempnp.ravel()
    dataframe_gradient_Y = np.gradient(tempnp)
    
    x = dataframeInput[['X']].loc[2]
    y = dataframeInput[['Y']].loc[2]
    print(x)
    print(y)
    euclideanNorm = math.hypot(x, y)
    print(euclideanNorm)
    return dataframe_gradient_X, dataframe_gradient_Y
    
def calculateVector(dataframeInput):
    #####################Separate clusters for mean calculation################################
    tempNP_splitter = []
    pivot = 0
    pivoted_cluster_id = dataframeInput[['TrackID']].loc[pivot]
    pivoted_cluster_id = pivoted_cluster_id.TrackID
    while pivot < len(dataframeInput):        
        current_cluster_id = dataframeInput[['TrackID']].loc[pivot]
        current_cluster_id = current_cluster_id.TrackID
        if current_cluster_id != pivoted_cluster_id:
            tempNP_splitter += [pivot]
            pivoted_cluster_id = current_cluster_id
        pivot += 1
    
    counter = 0
    current_pivot = 0
    visualize_np_X = np.empty(0)
    visualize_np_Y = np.empty(0)
    average_np_X = np.empty(0)
    average_np_Y = np.empty(0)
    
    while counter <= len(tempNP_splitter):
        try:
            tempDF_X, tempDF_Y = calculateGradient(dataframeInput[current_pivot:tempNP_splitter[counter]])

        except:
            tempDF_X, tempDF_Y = calculateGradient(dataframeInput[current_pivot:(dataframeInput.iloc[-1].name + 1)])
        try:
            current_pivot = tempNP_splitter[counter]
        except:
            current_pivot = 0
        visualize_np_X = np.append(visualize_np_X, tempDF_X)
        visualize_np_Y = np.append(visualize_np_Y, tempDF_Y)
        tempDF_X = np.mean(tempDF_X)
        tempDF_Y = np.mean(tempDF_Y)
        average_np_X = np.append(average_np_X, tempDF_X)
        average_np_Y = np.append(average_np_Y, tempDF_Y)
        counter += 1

    ###########################################################################################
    
    ################## Average gradient for each cluster##############
    temp_grad_X = pd.DataFrame.mean(dataframeInput[['X']], axis = 0)
    temp_grad_Y = pd.DataFrame.mean(dataframeInput[['Y']], axis = 0)
    ##################################################################
    
    
    ######################## Plotting ###################################
    plt.gca().invert_yaxis()
    plt.quiver(dataframeInput[['X']], dataframeInput[['Y']], visualize_np_X, visualize_np_Y)
#     plt.quiver(average_np_X, average_np_Y)
    plt.show()
    #####################################################################
    return average_np_X, average_np_Y