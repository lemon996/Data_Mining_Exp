#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

# AGNES算法："自底向上"聚合策略的层次聚类算法
# 1、将数据集中的每一个样本作为一个初始聚类簇
# 2、找出距离最近的两个聚类簇进行合并
# 3、不断重复步骤2，直至达到预设的聚类簇个数


data = '''
1,0,2,
2,0,0,
3,1.5,0,
4,5,0,
5,5,2,
'''

# 加载数据集
def load_dataset(data):
    data_ = data.strip().split(',')
    dataset = [(float(data_[i]), float(data_[i + 1]))
               for i in range(1, len(data_) - 1, 3)]
    return dataset

# 展示聚类前数据集分布
def show_dataset(dataset):
    for item in dataset:
        plt.plot(item[0], item[1], 'ob')
    plt.title("Dataset")
    plt.show()

# 计算两点之间的欧氏距离并返回
def elu_distance(a, b):
    dist = np.sqrt(np.sum(np.square(np.array(a) - np.array(b))))
    return dist

# 计算集合Ci, Cj间最小距离并返回
def dist_min(ci, cj):
    return min(elu_distance(i, j) for i in ci for j in cj)

# 计算集合Ci, Cj间最大距离并返回
def dist_max(ci, cj):
    return max(elu_distance(i, j) for i in ci for j in cj)

# 计算集合Ci, Cj间平均距离并返回
def dist_avg(ci, cj):
    return sum(elu_distance(i, j)
               for i in ci for j in cj) / (len(ci) * len(cj))

# 找出距离最小的两个簇并返回
def find_index(m):
    min_dist = float('inf')
    x = y = 0
    for i in range(len(m)):
        for j in range(len(m[i])):
            if i != j and m[i][j] < min_dist:
                min_dist, x, y = m[i][j], i, j
    return x, y, min_dist

def agnes(dataset, dist, k):
    # 初始化聚类簇及距离矩阵
    c, m = [], []
    # 将数据集中的每一个样本作为一个初始聚类簇
    for item in dataset:
        ci = []
        ci.append(item)
        c.append(ci)
    # 基于某种集合间距离计算方式计算簇类间距离
    for i in c:
        mi = []
        for j in c:
            mi.append(dist(i, j))
        m.append(mi)
    q = len(dataset)

    # 自底向上聚合
    while q > k:
        # 找出距离最近的两个聚类簇进行合并
        x, y, min_dist = find_index(m)
        # 注意extend与append的区别
        c[x].extend(c[y])
        # 更新聚类簇
        c.remove(c[y])
        # 重新计算聚类簇间距离
        m = []
        for i in c:
            mi = []
            for j in c:
                mi.append(dist(i, j))
            m.append(mi)
        q -= 1
    print(c)
    return c


# 展示聚类结果
def show_cluster(cluster):
    # 展示聚类结果
    colors = ['or', 'ob', 'og', 'ok', 'oy', 'ow']
    for i in range(len(cluster)):
        for item in cluster[i]:
            plt.plot(item[0], item[1], colors[i])
    plt.title("AGNES Clustering")
    plt.show()

# 程序执行入口

if __name__ == "__main__":
    dataset = load_dataset(data)
    show_dataset(dataset)
    k = 2
    cluster = agnes(dataset, dist_avg, k)
    show_cluster(cluster)
