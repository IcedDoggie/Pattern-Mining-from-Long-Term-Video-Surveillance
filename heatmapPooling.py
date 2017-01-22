# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:40:59 2017

@author: Ice
"""

def heatmapPooling(heatmapArray, pooling_dim):
    array_of_pooled_images = []
    yDim = heatmapArray.shape[0]
    xDim = heatmapArray.shape[1]
    pool_i = 0
    start_i = 0
    
    # pooling from top to bottom
    while start_i < yDim:
        pool_j = 0
        start_j = 0
        pool_i += pooling_dim
        while start_j < xDim:
            pool_j += pooling_dim
            pooled_image = heatmapArray[start_i:pool_i, start_j:pool_j]
            array_of_pooled_images += [pooled_image]
            start_j = pool_j
        start_i = pool_i
        
    start_i = 0
    pool_i = 0
    array_of_pooled_images_topbottom = []
    
    # pooling from left to right
    while start_i < xDim:
        pool_j = 0
        start_j = 0
        pool_i += pooling_dim
        while start_j < yDim:
            pool_j += pooling_dim
            pooled_image = heatmapArray[start_j:pool_j, start_i:pool_i]
            array_of_pooled_images_topbottom += [pooled_image]
            start_j = pool_j
#             print(start_j)
        start_i = pool_i
        
    array_of_pooled_images = np.array(array_of_pooled_images)
    array_of_pooled_images_topbottom = np.array(array_of_pooled_images_topbottom)
    vector_array_pooled_images = np.concatenate(array_of_pooled_images)
    vector_array_pooled_images = np.concatenate(vector_array_pooled_images)
    
#     print((array_of_pooled_images))
   
    
#     sum_array = np.sum(array_of_pooled_images)
    rowCounter = 0
#     sum_array = np.empty([array_of_pooled_images.shape[0], 2])
    sum_array = []
    sum_array_top_bottom = []
    
    while rowCounter < array_of_pooled_images.shape[0]:
        sum_of_pool = array_of_pooled_images[rowCounter]
        sum_of_pool_top_bottom = array_of_pooled_images_topbottom[rowCounter]
#         np.set_printoptions(threshold=np.nan)
#         print(array_of_pooled_images[rowCounter].max())
#         print(array_of_pooled_images[rowCounter])
        sum_of_pool = np.sum(sum_of_pool)
        sum_of_pool_top_bottom = np.sum(sum_of_pool_top_bottom)
          # log function
#         sum_of_pool = np.add(sum_of_pool, 1)
#         sum_of_pool = np.log(sum_of_pool)
#         print(sum_of_pool)

#         sum_array = np.insert(sum_array, [rowCounter, 2], [rowCounter+1,sum_of_pool])
        sum_array += [(rowCounter),(sum_of_pool)]
        sum_array_top_bottom += [(rowCounter), (sum_of_pool_top_bottom)]
        rowCounter += 1
#     print("new array")
    sum_array = np.asarray(sum_array)
    sum_array_top_bottom = np.asarray(sum_array_top_bottom)
#     print(sum_array.shape)
    sum_array = np.reshape(sum_array, (int(sum_array.shape[0])/2,2))
    sum_array_top_bottom = np.reshape(sum_array_top_bottom, (int(sum_array_top_bottom.shape[0])/2,2))
    sum_array = np.transpose(sum_array)
    sum_array_top_bottom = np.transpose(sum_array_top_bottom)
    sum_array = sum_array[1]
    sum_array_top_bottom = sum_array_top_bottom[1]
#     sum_array_transpose = sum_array.transpose()
#     print(sum_array_transpose)
    
    return vector_array_pooled_images, sum_array, sum_array_top_bottom