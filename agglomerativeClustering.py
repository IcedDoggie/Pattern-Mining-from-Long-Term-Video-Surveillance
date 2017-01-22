# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 20:40:23 2017

@author: Ice
"""

def agglomerativeClustering(heatmapArray, feature_vector):
    model_ac = AgglomerativeClustering(n_clusters = 2, affinity = 'euclidean', linkage = 'ward')
    cluster_labels = model_ac.fit_predict(feature_vector)
    params = model_ac.get_params(deep=True)
    linkage_cluster = hierarchy.linkage(feature_vector, 'ward')
    
    plt.title('Agglomerative Clustering On Trajectory Data Pool')
    plt.xlabel('Footsteps Count')
    plt.ylabel('Number of Days')
#     dendrogram = hierarchy.dendrogram(linkage_cluster, p= 5, truncate_mode='level', color_threshold=50, show_leaf_counts=False)
#     dendrogram = hierarchy.dendrogram(linkage_cluster)
    max_d = 3000
    dendrogram = fancy_dendrogram(linkage_cluster, p=6, truncate_mode='level', show_leaf_counts = False, max_d=max_d)
    clusters = hierarchy.fcluster(linkage_cluster, max_d, criterion='distance')
#     plt.savefig('Fancy Dendrogram.png')
    plt.show()
    print((clusters))
    print((cluster_labels))
    
    # create x-axis
    counter_x = 0
    x_axis = []
    feature_axis = []
    feature_axis_counter = collections.Counter(cluster_labels)
    while counter_x < len(feature_axis_counter):
        x_axis += [counter_x]
        feature_axis += [feature_axis_counter[counter_x]]
        counter_x += 1
    
    
    plt.hist(x_axis, feature_axis)
    plt.show()
#     plt.savefig('scatterplot for clustering')
#     plt.show()
#     print(feature_vector)
#     print(cluster_labels)
#     print(params)
    