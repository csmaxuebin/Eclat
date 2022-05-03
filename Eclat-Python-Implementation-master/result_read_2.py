def Read_Data(filename):
    data = []
    f = open(filename, 'r', encoding="utf8")
    for row in f:
        rr = row.split(" ")
        # print(rr)
        data.append(rr[1])
    f.close()
    return data


def Read_noise_Data(filename):
    data = []
    re_error = []
    f = open(filename, 'r', encoding="utf8")
    for row in f:
        rr = row.split(" ")
        data.append([rr[1], int(rr[3]), rr[7]])
        re_error.append([rr[3], rr[7]])
    f.close()
    return data, re_error


def get_median(data):
    data = sorted(data)
    size = len(data)
    if size % 2 == 0:   # 判断列表长度为偶数
        median = (data[size//2]+data[size//2-1])/2
        data[0] = median
    if size % 2 == 1:   # 判断列表长度为奇数
        median = data[(size-1)//2]
        data[0] = median
    return data[0]


if __name__ == '__main__':
    F_Score_result = []
    Re_error_result = []
    data = Read_Data("retail_0.04.csv")  # 取出的是频繁项集的名称

    F_sum = 0
    Re_sum = 0
    for i in range(1, 11):

        noise_data_read = 'retail_0.04_noise_' + str(i) + '.csv'
        noise = Read_Data(noise_data_read)

        U = len(set(data) & set(noise))
        UP = len(set(noise))
        UC = len(set(data))
        precision = U / UP
        recall = U / UC
        F_SCORE = 2 * (precision * recall) / (precision + recall)
        F_Score_result.append(F_SCORE)
    for i in F_Score_result:
        F_sum += i
        print(i)
    print('mushroom的平均F-Score为：', F_sum/len(F_Score_result))

    for i in range(1, 11):
        noise_data_read = 'retail_0.04_noise_' + str(i) + '.csv'
        noise_data, re = Read_noise_Data(noise_data_read)
        re_list = []
        for i in range(len(re)):
            # print(re[i][1], re[i][0])
            if float(re[i][0]) == 0:
                continue
            else:
                re_list.append(abs(float(re[i][1])) / float(re[i][0]))
        median = get_median(re_list)  # median 为相对误差
        Re_error_result.append(median)
    for j in Re_error_result:
        Re_sum += j
        print("re", j)
    print('mushroom的平均re为：', Re_sum/len(Re_error_result))

