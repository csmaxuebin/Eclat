candiate_item = []
FreqItems = dict()
ab_list = []
support = 0
def eclat(prefix, items, prefix_support):  # 挖掘阶段
    global isupp
    while items:
        i, itids = items.pop(0)
        itids = list(itids)
        if itids[0] == 0:
            isupp = len(itids) - 1  # 这个部分加入预剪枝
        elif itids[0] == 1:
            isupp = prefix_support - len(itids) + 1
        if isupp >= minsup:  # 将这个判断转换为预剪枝的判断， item中的都是频繁项集，只需判断能否用于生成k+1项集即可。

            FreqItems[frozenset(prefix + [i])] = isupp  # frozenset集合是不可变的 # 这部分是频繁k项集
            suffix = []
            tidset = []
            diffset = []
            for j, ojtids in items:  # 这部分可以对交集的第二部分进行预剪枝
                j_set, j_support = support_compute(isupp, itids, list(ojtids))
                print(j_set, j, itids, ojtids, j_support)
                print('-----------')
            # jtids = itids & ojtids  # 这部分交集产生的是候选k+1项集，对候选项集进行后剪枝
            # # 坐交集操作的时候可以引入diffset
            # if len(jtids) >= minsup:
                if j_support >= minsup:
                    if j_set[0] == 0:
                        tidset.append((j, j_set))
                    elif j_set[0] == 1:
                        diffset.append((j, j_set))
                    # suffix.append((j, j_set))  # 这部分交集产生的是候选k+1项集，对候选项集进行后剪纸
                    # print(suffix)
            tidset = sorted(tidset, key=lambda item: len(item[1]), reverse=False)
            diffset = sorted(diffset, key=lambda item: len(item[1]), reverse=True)

            eclat(prefix + [i], tidset + diffset, isupp)

            # print(sorted(suffix, key=lambda item: len(item[1]), reverse=True))
            # print('-----------')
            # eclat(prefix + [i], sorted(suffix, key=lambda item: len(item[1]), reverse=True), isupp)


def support_compute(a_list_support, a_list, b_list):
    if a_list[0] == 0:
        if b_list[0] == 0:  # 两个都是tidset
            ab_set1 = set(a_list) & set(b_list)  # ab_set1 是tidset
            ab_set2 = set(i for i in a_list if i not in b_list)  # ab_set2 是diffset
            if len(ab_set1) <= len(ab_set2) + 1:
                ab_set = ab_set1
                ab_list = list(ab_set)  # ab_set 是 tidset
                support = len(ab_list) - 1
            elif len(ab_set2) + 1 < len(ab_set1):
                ab_set = ab_set2
                ab_list = list(ab_set)  # ab_set 是 diffset
                ab_list.insert(0, 1)
                support = a_list_support - len(ab_list) + 1
        if b_list[0] == 1:  # 一个tidset 一个diffset
            ab_set = set(a_list) & set(b_list)
            ab_list = list(ab_set)
            ab_list.insert(0, 1)  # ab_list 是 diffset
            support = a_list_support - len(ab_list) + 1
    if a_list[0] == 1:  # 两个diffset
        ab_list = [i for i in b_list if i not in a_list]
        ab_list.insert(0, 1)  # ab_list 是 diffset
        support = a_list_support - len(ab_list) + 1 # 这块支持度计算错误
    return ab_list, support


def print_Frequent_Itemsets(output_FreqItems, FreqItems):
    file = open(output_FreqItems, 'w+')
    for item, support in FreqItems.items():
        file.write(" {} : {} \n".format(list(item), round(support, 4)))


def Read_Data(filename, delimiter=' '):  # 预处理 将水平格式转换为垂直格式
    data = {}
    trans = 0
    f = open(filename, 'r', encoding="utf8")
    for row in f:
        trans += 1
        for item in row.rstrip("\n").rstrip(" ").split(delimiter):
            if item not in data:
                data[item] = set()
                data[item].add(0)  # 读取数据的时候为集合分配tidset与diffset的辨识位
            data[item].add(trans)
    f.close()
    return data


if __name__ == "__main__":
    # minsup = 3
    # output_FreqItems = 'output_freqitems2.csv'
    # dict_id = 0
    # data = Read_Data('input.txt', ' ')  # change the delimiter based on your input file
    # for k, v in list(data.items()):  # 第一步筛选出频繁项
    #     if len(v) - 1 < minsup:
    #         del data[k]
    # print('finished reading data..... \n Starting mining .....')
    # # print(sorted(data.items(), key=lambda item: len(item[1]), reverse=False))
    # eclat([], sorted(data.items(), key=lambda item: len(item[1]), reverse=False), dict_id)  # 根据字典中值的大小，对字典中的项排序
    # print('found %d Frequent items' % len(FreqItems))
    # print_Frequent_Itemsets(output_FreqItems, FreqItems)
    for i in range(0, 5):
        print(i)

