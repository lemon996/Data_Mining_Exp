#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import numpy as np
import random
import matplotlib.pyplot as plt

# DBSCAN算法：基于密度可达关系导出最大密度相连样本集合
# 1、根据给定的邻域参数（e, min_points）找出所有的核心对象
# 2、以任一核心对象为出发点，找出由其密度可达的样本生成聚类簇
# 3、当所有核心对象均被访问过时停止运行

data = '''
1,1,3,
2,1,2,
3,2,4,
4,2,3,
5,2,2,
6,2,1,
7,3,2,
8,4,2,
9,5,3,
10,5,2,
11,5,1,
12,6,2
'''

# 加载数据集

def load_dataset(data):
    data_ = data.strip().split(',')
    dataset = [(float(data_[i]), float(data_[i + 1]))
               for i in range(1, len(data_) - 1, 3)]
    print(dataset)
    return dataset

# 展示聚类前数据集分布

def show_dataset(dataset):
    for item in dataset:
        plt.plot(item[0], item[1], 'og')
    plt.title("Dataset")
    plt.show()

#  计算两个点之间欧氏距离

def elu_distance(a, b):
    dist = np.sqrt(np.sum(np.square(np.array(a) - np.array(b))))
    return dist

def dbscan(dataset, e, min_points):
    k = 0           # 聚类个数
    omega = set()   # 核心对象集合
    not_visit = set(dataset)    # 未访问样本集合
    cluster = dict()            # 聚类结果

    # 遍历样本集找出所有核心对象
    for di in dataset:
        if len([dj for dj in dataset if elu_distance(di, dj) <= e]) \
                >= min_points:
            omega.add(di)

    while len(omega):
        # 记录当前未访问样本集合
        not_visit_old = not_visit
        # 随机选取一个核心对象core
        core = list(omega)[random.randint(0, len(omega) - 1)]
        not_visit = not_visit - set(core)
        # 初始化队列，存放核心对象或样本
        core_deque = []
        core_deque.append(core)

        while len(core_deque):
            coreq = core_deque[0]
            # 找出以coreq邻域内的样本点
            coreq_neighborhood = [di for di in dataset
                                  if elu_distance(di, coreq) <= e]

            # 若coreq为核心对象，则通过求交集方式将其邻域内且未被访问过的样本找出
            if len(coreq_neighborhood) >= min_points:
                intersection = not_visit & set(coreq_neighborhood)
                core_deque += list(intersection)
                not_visit = not_visit - intersection

            core_deque.remove(coreq)
        k += 1
        Ck = not_visit_old - not_visit
        omega = omega - Ck
        cluster[k] = list(Ck)
        print(k, '簇的数目：', len(cluster[k]))
        print(cluster[k])
    return cluster

# 展示聚类结果

def show_cluster(cluster):
    colors = ['og', 'ob', 'or', 'ok', 'oy', 'ow']
    for key in cluster.keys():
        for item in cluster[key]:
            plt.plot(item[0], item[1], colors[key])
    plt.title("DBSCAN Clustering")
    plt.show()


# 程序执行入口

if __name__ == "__main__":
    dataset = load_dataset(data)
    show_dataset(dataset)
    r, min_points = 1, 4
    cluster = dbscan(dataset, r, min_points)
    show_cluster(cluster)
