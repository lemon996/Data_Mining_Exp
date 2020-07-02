# -*- coding: UTF-8 -*-

# 从外部文件data.txt导入数据集
def load_data_set():
    data_set = []
    # 读取数据
    fd = open("data.txt", "r")
    # 处理数据
    for line in fd.readlines():
        # 先按行分割字符串
        line = line.strip('\n')
        # 再按列分割字符串
        data_set.append(list(line.split(', ')))
    return data_set

# 从数据集构造1-候选集
def create_C1(data_set):
    C1 = set()
    for t in data_set:
        for item in t:
            # frozenset可hash利于排序
            item_set = frozenset([item])
            C1.add(item_set)
    return C1

# 判断是否满足
def is_apriori(Ck_item, Lksub1):
    for item in Ck_item:
        sub_Ck = Ck_item - frozenset([item])
        if sub_Ck not in Lksub1:
            return False
    return True

# 生成各个候选集Ck
def create_Ck(Lksub1, k):
    Ck = set()
    len_Lksub1 = len(Lksub1)
    list_Lksub1 = list(Lksub1)
    for i in range(len_Lksub1):
        for j in range(1, len_Lksub1):
            l1 = list(list_Lksub1[i])
            l2 = list(list_Lksub1[j])
            l1.sort()
            l2.sort()
            if l1[0:k-2] == l2[0:k-2]:
                Ck_item = list_Lksub1[i] | list_Lksub1[j]
                if is_apriori(Ck_item, Lksub1):
                    Ck.add(Ck_item)
    return Ck

# 通过候选集Ck生成频繁集Lk
def generate_Lk_by_Ck(data_set, Ck, min_support, support_data):
    Lk = set()
    item_count = {}
    for t in data_set:
        for item in Ck:
            if item.issubset(t):
                if item not in item_count:
                    item_count[item] = 1
                else:
                    item_count[item] += 1
    # 转换成浮点数，便于求支持度
    t_num = float(len(data_set))
    for item in item_count:
        if (item_count[item] / t_num) >= min_support:
            Lk.add(item)
            support_data[item] = item_count[item] / t_num
    return Lk

# 生成各频繁项集，最小支持度为0.5
def generate_L(data_set, k, min_support):
    support_data = {}
    # 创建候选1项集
    C1 = create_C1(data_set)
    # 通过候选项1集生成频繁1项集
    L1 = generate_Lk_by_Ck(data_set, C1, min_support, support_data)
    Lksub1 = L1.copy()
    L = []
    L.append(Lksub1)
    for i in range(2, k+1):
        Ci = create_Ck(Lksub1, i)
        Li = generate_Lk_by_Ck(data_set, Ci, min_support, support_data)
        Lksub1 = Li.copy()
        L.append(Lksub1)
    return L, support_data

# 生成从频繁集关联规则分析
def generate_big_rules(L, support_data, min_conf):
    strong_rule_list = []  # 保存强关联规则
    sub_set_list = []   #
    for i in range(0, len(L)):
        for freq_set in L[i]:
            for sub_set in sub_set_list:
                if sub_set.issubset(freq_set):
                    conf = support_data[freq_set] \
                           / support_data[freq_set - sub_set]
                    big_rule = (freq_set - sub_set, sub_set, conf)
                    if conf >= min_conf and big_rule not in strong_rule_list:
                        strong_rule_list.append(big_rule)
            sub_set_list.append(freq_set)
    return strong_rule_list

if __name__ == "__main__":
    # 加载数据集
    data_set = load_data_set()
    # 生成频繁项集及支持度集
    L, support_data = generate_L(data_set, k=3, min_support=0.5)
    # 生成强关联规则
    strong_rules_list = generate_big_rules(L, support_data, min_conf=0.7)
    print ('最小支持度: 0.5\t最小置信度: 0.7')
    # 遍历处理好的频繁项集
    for Lk in L:
        print ("频繁" + str(len(list(Lk)[0])) + "项集") # 输出各频繁项集
        for freq_set in Lk:
            fset = []   # 转换成set
            for i in freq_set:  # 导入到新set
                fset.append(i)
            print (fset, '\t支持度:', support_data[freq_set]) # 输出

    print("强关联规则")
    # 转换成set
    for item in strong_rules_list:
        item0, item1 = [], []
        for i in item[0]:
            item0.append(i)
        for i in item[1]:
            item1.append(i)
        # 输出强关联规则及置信度
        print (item0, "=>", item1, '\t置信度:', item[2])

