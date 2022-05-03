from treelib import Tree
from fractions import Fraction
from itertools import combinations
import random
import numpy as np
import sys
sys.setrecursionlimit(100000000)  # 扩大递归的深度
privacy_budget = [0]
frequent_itemset = [[0]]  # 存储频繁项集的二维数组
candidate_itemset = []  # 存储候选项集的二维数组

class Tree_node(object):
    def __init__(self, member_prefix, member_list):
        self.member_prefix = member_prefix
        self.member_list = member_list


class itemset(object):
    def __init__(self, content, tidset_or_diffset, support):
        self.content = content
        self.tidset_or_diffset = tidset_or_diffset
        self.support = support


def Read_Data(filename, delimiter=' '):  # 预处理 将水平格式转换为垂直格式
    data = {}
    trans = 0
    f = open(filename, 'r', encoding="utf8")
    for row in f:
        trans += 1
        for item in row.rstrip("\n").rstrip(" ").split(delimiter):   # rstrip(" ")删除字符最右边的空格
            item_i = "I" + item
            if item_i not in data:
                data[item_i] = set()
                data[item_i].add(0)  # 读取数据的时候为集合分配tidset与diffset的辨识位
            data[item_i].add(trans)
    f.close()
    return data


def print_Frequent_Itemsets(output_FreqItems, FreqItems):
    file = open(output_FreqItems, 'w+')
    for i in range(1, len(FreqItems)):
        for Fre in FreqItems[i]:
            file.write(" {} : {} : {} : {} \n".format(Fre[0], Fre[1], Fre[2], Fre[3]))  # 加噪写入文件
            # file.write(" {} : {} \n".format(Fre[0], Fre[1]))  # 不加噪写入文件

def budget_allocation(epsilon, tree_depth):  # 等价类树中的层间的隐私预算分配 *小数形式
    w = 0
    for i in range(1, tree_depth):
        w += 1 / (tree_depth - (i - 1))
    epsilon_u = epsilon / w
    for i in range(1, tree_depth):
        privacy_budget.append(epsilon_u * (1 / (tree_depth - (i - 1))))
    privacy_budget.reverse()
# def budget_allocation(epsilon, tree_depth):  # 等价类树中的层间的隐私预算分配  *分数形式
#     d = tree_depth
#     w = 0
#     for j in range(1, tree_depth):
#         w += Fraction(1, d - (j - 1))
#     epsilon_u = Fraction(epsilon, w)
#     for u in range(1, tree_depth):
#         privacy_budget.append(epsilon_u * Fraction(1, d - (u - 1)))


def TidsetOrDiffset(a_list, b_list):   # 用于定义项集的tidset或者diffset
    if a_list[0] == 0:
        if b_list[0] == 0:  # 两个都是tidset
            del a_list[0]
            del b_list[0]
            aa_list = set(a_list)
            bb_list = set(b_list)
            ab_set1 = aa_list & bb_list  # ab_set1 是tidset
            ab_set2 = set(i for i in aa_list if i not in bb_list)  # ab_set2 是diffset
            if len(ab_set1) <= len(ab_set2):
                ab_set = ab_set1
                ab_list = list(ab_set)  # ab_set 是 tidset
                ab_list.insert(0, 0)
                return ab_list
            elif len(ab_set2) < len(ab_set1):
                ab_set = ab_set2
                ab_list = list(ab_set)  # ab_set 是 diffset
                ab_list.insert(0, 1)
                return ab_list
        if b_list[0] == 1:  # 一个tidset 一个diffset
            del a_list[0]
            del b_list[0]
            aa_list = set(a_list)
            bb_list = set(b_list)
            ab_set = aa_list & bb_list
            ab_list = list(ab_set)
            ab_list.insert(0, 1)  # ab_list 是 diffset
            return ab_list
    if a_list[0] == 1:  # 两个diffset
        del a_list[0]
        del b_list[0]
        aa_list = set(a_list)
        bb_list = set(b_list)
        ab_list = [i for i in bb_list if i not in aa_list]
        ab_list.insert(0, 1)  # ab_list 是 diffset
        return ab_list


def find_subset(candidateSet):  # 用于找到一个项集的所有子集
    subset = []
    realsubset = []
    for i in range(1, len(candidateSet) + 1):
        subset.extend(list(combinations(candidateSet, i)))
    subset.pop()

    for j in subset:
        ch = ""
        for char in range(len(j)):
            ch = ch + j[char]
        realsubset.append(ch)

    return realsubset


def pre_prune(frequent_low_itemset, k):  # 对项集中的每个项出现的次数进行计数
    single_item = {}
    prune_item = []
    for i in frequent_low_itemset:
        for j in i[0]:
            if j not in single_item:
                single_item[j] = 1
            else:
                single_item[j] += 1
    for c in single_item:
        if single_item[c] < k - 1:
            prune_item.append("I" + c)
    return prune_item


def post_prune_1(candidate_i):   # 后剪枝中的第一个
    candidate_subset = find_subset(candidate_i)
    if len(candidate_i) == 1:
        return True
    frequent_i_low = []
    for i in range(1, len(candidate_i)):
        for frequent_i in frequent_itemset[len(candidate_i) - i]:
            frequent_i_low.append(frequent_i[0])
    for s in candidate_subset:
        if s not in frequent_i_low:
            return False
    return True


def post_prune_2(candidate_i):  # 后剪枝中的第二个
    if len(candidate_i) == 1:
        return True
    randint_i = random.randint(1, len(candidate_i) - 1)
    pre_i = candidate_i[: randint_i]
    single_item = {}
    for i in frequent_itemset[len(candidate_i) - 1]:
        for pre_i in i[0]:
            if pre_i not in single_item:
                single_item[pre_i] = 1
            else:
                single_item[pre_i] += 1
    if single_item[pre_i] < len(candidate_i) - randint_i:
        return False
    else:
        return True


def support_compute(parent_support, current_itemset_tidset_or_diffset):  # 项集支持度的计算
    if current_itemset_tidset_or_diffset[0] == 0:  # current_list 为tidset
        current_support = len(current_itemset_tidset_or_diffset) - 1  # 减一为了减去标识位
        return current_support
    elif current_itemset_tidset_or_diffset[0] == 1:  # current_list 为diffset
        current_support = parent_support - len(current_itemset_tidset_or_diffset) + 1
        return current_support


def DpEclat(sub_root_list, level, candidate_n):   # 构建等价类树 sub_root_list就是频繁低项集所代表的的节点
    sub_sub_root_list = []
    frequent_i_itemset = []
    candidate_i_num = 0
    if len(sub_root_list) > 0:
        # print(sub_root_list)
        each_branch_privacy = privacy_budget[level - 1]  # 每个分支的隐私预算均为当前层次的隐私预算
        for sub_root in sub_root_list:
            # print(sub_root.data.member_prefix[0].content, sub_root.data.member_prefix[0].support)
            member_list = sub_root.data.member_list
            prefix = sub_root.data.member_prefix[0].content
            prefix_list = sub_root.data.member_prefix[0].tidset_or_diffset
            prefix_support = sub_root.data.member_prefix[0].support
            if len(member_list):  # member_list 是候选低项集
                skk = 10000  # 功能同sk
                for tree_item in member_list[::-1]:  # 使用[::-1]实现由右向左的构建树
                    # 这部分进行后剪枝
                    if len(prefix + tree_item.content) > 2:
                        sub_root_content_list = []
                        list_without_I = (prefix + tree_item.content).split("I")
                        for i in range(1, len(list_without_I)):
                            sub_root_content_list.append("I" + list_without_I[i])
                        tip1 = post_prune_1(sub_root_content_list)
                        tip2 = post_prune_2(sub_root_content_list)
                    if tip1 and tip2:
                        each_branch_sensitive = candidate_n   # 敏感度取当前层次敏感度
                        # each_branch_sensitive = len(member_list)
                        each_lamuda = each_branch_sensitive / each_branch_privacy
                        each_noise = np.random.laplace(0, each_lamuda)
                        tree_item_support = support_compute(prefix_support, tree_item.tidset_or_diffset)
                        tree_item_noise_support = tree_item_support + each_noise  #  加噪之后的支持度
                        if tree_item_noise_support < minsup:
                            del member_list[member_list.index(tree_item)]  # 如果不满足则删除，使敏感度随之降低
                            continue
                        frequent_i_itemset.append([prefix + tree_item.content, tree_item_support, tree_item_noise_support, each_noise])
                        # frequent_i_itemset.append([prefix + tree_item.content, tree_item_support])
                        print(prefix + tree_item.content, tree_item_support, each_branch_sensitive, each_branch_privacy)
                        skk += 1
                        if tree_item != member_list[len(member_list) - 1]:
                            sub_sub_candidate = []
                            item_i = prefix + tree_item.content
                            tree_item_list = tree_item.tidset_or_diffset  # 这个位置根据类成员的tideset或diffset进行类成员的裁剪
                            tidset = []
                            diffset = []
                            # item_it_tidset = list(TidsetOrDiffset(list(prefix_list), list(tree_item_list)))  # 构建树的时候将tidset与diffset进行引入
                            item_ii = itemset(item_i, tree_item_list, tree_item_support)  # 将类成员的tidset或diffset赋给子节点的前缀
                            for candidata_item in member_list[member_list.index(tree_item) + 1:]:
                                candidata_tidset_or_diffset = TidsetOrDiffset(list(item_ii.tidset_or_diffset), list(candidata_item.tidset_or_diffset))
                                candidata_item_support = support_compute(tree_item_support, candidata_tidset_or_diffset)
                                if candidata_tidset_or_diffset[0] == 0:
                                    candidata = itemset(candidata_item.content, candidata_tidset_or_diffset, candidata_item_support)
                                    tidset.append(candidata)
                                elif candidata_tidset_or_diffset[0] == 1:
                                    candidata = itemset(candidata_item.content, candidata_tidset_or_diffset, candidata_item_support)
                                    diffset.append(candidata)
                            tidset = sorted(tidset, key=lambda t_item: len(t_item.tidset_or_diffset), reverse=False)
                            diffset = sorted(diffset, key=lambda d_item: len(d_item.tidset_or_diffset), reverse=True)
                            next_list = tidset + diffset
                            next_item_set = Tree_node([item_ii], next_list)  # 将这个位置中member_list中的tidsetOrDiffset修改为候选项集
                            candidate_i_num += len(next_list)
                            larger_item = tree.create_node(str(skk) + str(item_ii.content), item_ii.content, data=next_item_set, parent=sub_root.identifier)
                            sub_sub_candidate.append(larger_item)
                            for sub_candidate in sub_sub_candidate:
                                sub_sub_root_list.append(sub_candidate)
                        elif tree_item == member_list[len(member_list) - 1]:
                            leaf_item_i = prefix + tree_item.content
                            tree_item_list = tree_item.tidset_or_diffset
                            leaf_item_it_tidset = list(TidsetOrDiffset(list(prefix_list), list(tree_item_list)))
                            leaf_item_ii = itemset(leaf_item_i, leaf_item_it_tidset, tree_item_support)
                            leaf_item_set = Tree_node([leaf_item_ii], [])
                            leaf_larger_item = tree.create_node(str(skk) + str(leaf_item_ii.content), leaf_item_ii.content, data=leaf_item_set, parent=sub_root.identifier)
                            sub_sub_root_list.append(leaf_larger_item)
                    else:
                        del member_list[member_list.index(tree_item)]  # 如果不满足则删除，使敏感度随之降低
                        continue
    else:
        return
    frequent_itemset.append(frequent_i_itemset)
    # 这部分加入预剪枝
    del_item = pre_prune(frequent_itemset[level], level)
    for j in sub_sub_root_list:
        for o in del_item:
            if o in j.identifier:
                del sub_sub_root_list[sub_sub_root_list.index(j)]
                break
            else:
                continue

    DpEclat(sub_sub_root_list, level + 1, candidate_i_num)


if __name__ == '__main__':
    minsup = 34333
    privacyBudget = 1  # 隐私预算需要分成两部分
    epsilon1 = privacyBudget/3  # 第一部分隐私预算用于挖掘频繁1项集
    epsilon2 = privacyBudget - epsilon1  # 第二部分隐私预算用于挖掘频繁k项集
    data = Read_Data('pumsb.txt', ' ')
    output_FreqItems = 'pumsb_0.7_noise_10.csv'
    lamuda1 = 74/epsilon1  # 挖掘1项集时的敏感度根据最大事务长度设定
    frequent_1_itemset = []
    noise_sup = minsup + np.random.laplace(0, lamuda1)
    for k, v in list(data.items()):  # 第一步筛选出频繁项
        v_support = len(v) - 1
        item_noise = np.random.laplace(0, lamuda1)  # loc=0.0 loc就是mu, scale=1.0 scale就是λ, size=None
        v_noise_support = v_support + item_noise  # 为每一个候选1项集进行加噪
        # print(k, v_noise_support)
        if v_noise_support < minsup:
            del data[k]
        else:
            frequent_1_itemset.append([k, v_support, v_noise_support, item_noise])
        # if v_noise_support < minsup:
        #     del data[k]
    frequent_itemset.append(frequent_1_itemset)
    c = []
    for item in data.items():
        item = itemset(item[0], item[1], len(item[1]) - 1)
        c.append(item)
    a = sorted(c, key=lambda ab: len(ab.tidset_or_diffset))  # 根据列表中元素的属性进行排序
    budget_allocation(epsilon2, len(a) + 1)  # 将隐私预算根据层次进行分配最后存到privacy_budget中
    tree_root = Tree_node({}, a)
    tree = Tree()
    tree.create_node("{}", "root", data=tree_root)  # root node
    sk = 10000  # sk用于解决树中分支无序的问题
    candidate_num = 0
    for item in a[::-1]:
        sk += 1
        if item == a[len(a) - 1]:
            item_set = Tree_node([item], [])
            last_item = tree.create_node(str(sk) + str(item.content), item.content, data=item_set, parent="root")
        elif item != a[len(a) - 1]:
            first_tidset = []
            first_diffset = []
            for first_member in a[a.index(item) + 1:]:
                first_tidset_or_diffset = list(TidsetOrDiffset(list(item.tidset_or_diffset), list(first_member.tidset_or_diffset)))
                if first_tidset_or_diffset[0] == 0:
                    first_t = itemset(first_member.content, first_tidset_or_diffset, len(first_tidset_or_diffset) - 1)  # 新建一个itemset防止上两行将原始的tidset进行重写
                    first_tidset.append(first_t)
                elif first_tidset_or_diffset[0] == 1:
                    first_d = itemset(first_member.content, first_tidset_or_diffset, item.support - len(first_tidset_or_diffset) + 1)
                    first_diffset.append(first_d)
            first_tidset = sorted(first_tidset, key=lambda t_item: len(t_item.tidset_or_diffset), reverse=False)
            first_diffset = sorted(first_diffset, key=lambda d_item: len(d_item.tidset_or_diffset), reverse=True)
            first_list = first_tidset + first_diffset
            item_set = Tree_node([item], first_list)  # 构建第一层节点是等价类成员就需要变成候选的多项集
            forward_item = tree.create_node(str(sk) + str(item.content), item.content, data=item_set, parent="root")
            candidate_num += len(first_list)
            # tree_build(forward_item)
    tc = tree.children("root")
    DpEclat(tc, 2, candidate_num)  # 由第2层开始
    print_Frequent_Itemsets(output_FreqItems, frequent_itemset)
    print(frequent_itemset)
    print("finish mining!")





