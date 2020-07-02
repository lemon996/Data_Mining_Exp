#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import numpy as np;
import pandas as pd

# 5个样本点之间的间距
mat = np.array([[0, 2, 2.5, 5.3, 5], [2, 0, 1.5, 5, 5.3]
                ,[2.5, 1.5, 0, 3.5, 4], [5.3, 5, 3.5, 0, 2.3]
                , [5, 5.3, 4, 2.3, 0]])

# 对每个样本点进行命名
all_elements = ['a', 'b', 'c', 'd', 'e']

# 将初始数据转换成相异矩阵
dissimilarity_matrix = pd.DataFrame(mat
                        , index=all_elements, columns=all_elements)

# 计算簇中每个点计算其平均距离
def avg_dissim_within_group_element(ele, element_list):
    max_diameter = -np.inf
    sum_dissm = 0
    for i in element_list:
        sum_dissm += dissimilarity_matrix[ele][i]
        if (dissimilarity_matrix[ele][i] > max_diameter):
            max_diameter = dissimilarity_matrix[ele][i]
    if (len(element_list) > 1):
        avg = sum_dissm / (len(element_list) - 1)
    else:
        avg = 0
    return avg

# 计算簇间每个点计算其平均距离
def avg_dissim_across_group_element(ele, main_list, splinter_list):
    if len(splinter_list) == 0:
        return 0
    sum_dissm = 0
    for j in splinter_list:
        sum_dissm = sum_dissm + dissimilarity_matrix[ele][j]
    avg = sum_dissm / (len(splinter_list))
    return avg

# 分裂器
def splinter(main_list, splinter_group):
    most_dissm_object_value = -np.inf
    most_dissm_object_index = None
    for ele in main_list:
        x = avg_dissim_within_group_element(ele, main_list)
        y = avg_dissim_across_group_element(ele, main_list, splinter_group)
        diff = x - y
        if diff > most_dissm_object_value:
            most_dissm_object_value = diff
            most_dissm_object_index = ele
    if (most_dissm_object_value > 0):
        return (most_dissm_object_index, 1)
    else:
        return (-1, -1)

# 将初始簇分裂成一个个簇
def split(element_list):
    main_list = element_list
    splinter_group = []
    (most_dissm_object_index, flag) = splinter(main_list, splinter_group)
    while (flag > 0):
        main_list.remove(most_dissm_object_index)
        splinter_group.append(most_dissm_object_index)
        (most_dissm_object_index, flag) = splinter(element_list, splinter_group)

    return (main_list, splinter_group)

# 寻找一个直径最大的簇心编号
def max_diameter(cluster_list):
    max_diameter_cluster_index = None
    max_diameter_cluster_value = -np.inf
    index = 0
    for element_list in cluster_list:
        for i in element_list:
            for j in element_list:
                if dissimilarity_matrix[i][j] > max_diameter_cluster_value:
                    max_diameter_cluster_value = dissimilarity_matrix[i][j]
                    max_diameter_cluster_index = index

        index += 1
    if (max_diameter_cluster_value <= 0):
        return -1
    return max_diameter_cluster_index

if __name__ == '__main__':
    current_clusters = ([all_elements])
    print('---------相异矩阵---------')
    print(mat)
    print('---------聚类结果---------')
    index, level = 0, 1
    while (index != -1):
        if level == 2:
            break
        print(level, current_clusters)
        (a_clstr, b_clstr) = split(current_clusters[index])
        del current_clusters[index]
        current_clusters.append(a_clstr)
        current_clusters.append(b_clstr)
        index = max_diameter(current_clusters)
        level += 1
    print(level, current_clusters)
