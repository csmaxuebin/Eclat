import numpy as np

# def Read_Data(filename, delimiter=' '):

#     data = {}
#     f = open(filename, 'r', encoding="utf8")
#     for row in f:
#         a = row.rstrip("\n").split(delimiter)
#         c = a[0].replace("\t", " ").split(" ")
#         item_i = int(c[0])
#         if item_i not in data:
#             data[item_i] = []
#             data[item_i].append(int(c[1]))
#         else:
#             data[item_i].append(int(c[1]))
#
#
#     f.close()
#     return data
#
#
# def print_file(filename, transaction):
#     file = open(filename, 'w+')
#
#     for item in transaction:
#         w = ""
#         for i in item:
#             w = w + str(i) + " "
#         print(w)
#         file.write(w)
#         file.write("\n")
#
# if __name__ == '__main__':
#     trans_list = []
#     data = Read_Data('BMS-POS.txt', ' ')
#     for v in data.values():
#         trans_list.append(v)
#     print_file("bms_pos.txt", trans_list)
#     print("finish writing!")
each_noise = np.random.laplace(0, 228, 50)
print(each_noise)