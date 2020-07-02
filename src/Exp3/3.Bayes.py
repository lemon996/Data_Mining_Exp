#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import pandas as pd
import numpy as np
import collections

# Bayes算法主体: 计算测试样本对应各个类别的概率
def bayes(feature, m, m_k, m_index, m_fk):
    # 得到测试样本的分类概率
    chance = {}
    for (key, value) in m_k.items():
        ll = len(feature)
        prob = 1.0
        for i in range(ll):
            t1 = m_index[feature[i]]
            t2 = m_fk[t1[1]]
            prob = round(prob * (t2[value[0]] + 1)
                         / (value[1] + t1[3])
                         / t1[2] * m, 10)
            if i == ll - 1:
                prob = round(prob * value[1] / m, 10)
                chance[key] = prob
    print(chance)
    return chance


# 构建训练集数据向量，以及对应分类标签
def trainDataSet():
    # 构建训练集数据，从.cvs文件中读取数据，最后一列为标签label，前面为训练集数据的特征feature
    csv_data = np.array(pd.read_csv('data.csv'))
    train_label = csv_data[:, 2]
    attr_count = len(csv_data[0])
    train_data = csv_data[:, 0:attr_count - 1]
    return train_data, train_label


def info(train_data, train_label):
    # 返回四个值: 样本总数m, 类别为k的字典表m_k
    # 特征X_i各个类别的取值数m_index
    # 类别为k,特征X_i各个类别的样本个数的表m_fk
    m = len(train_data)     # 样本总数m

    # 建立类别为k的字典表，key=(1,2...k)，
    # value为[类别k的实际名字,类别为k的样本数]
    m_k, k = {}, 0
    label_counter = collections.Counter(train_label)
    for (key, value) in label_counter.items():
        m_k[key] = [k, value]
        k += 1

    # 用一个字典表存储特征X_i各个类别的取值数, m_index
    # {key: [i:特征, sum:m_fk对应编号, value:该类别的取值数, len_i:特征i的个数]}
    m_index = {}
    sum = 0
    for i in range(len(train_data[0])):
        data_counter = collections.Counter(train_data[:, i])
        len_i = len(data_counter)
        for (key, value) in data_counter.items():
            m_index[key] = [i, sum, value, len_i]
            sum += 1
    print(m_index)

    # 创建一个二维数组m_fk存储m_ijk信息
    m_fk = np.zeros((len(m_index), len(m_k)))
    i = 0
    for (key, value) in m_index.items():
        m_ij = np.where(train_data[:, value[0]] == key, 1, 0)
        for j in range(len(m_ij)):
            if m_ij[j] == 1:
                # 查找疾病对应标签
                k = m_k[train_label[j]][0]
                m_fk[i][k] += 1
        i += 1
    return m, m_k, m_index, m_fk

if __name__ == "__main__":
    train_data, train_label = trainDataSet()
    m, m_k, m_index, m_fk = info(train_data, train_label)
    feature = []
    print('退出输入exit')
    while True:
        ss = input('输入:')
        if ss == 'exit':
            break
        feature.append(ss)
    probability = bayes(feature, m, m_k, m_index, m_fk)

