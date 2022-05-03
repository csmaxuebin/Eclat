def Read_Data(filename):
    data = []
    f = open(filename, 'r', encoding="utf8")
    for row in f:
        rr = row.split(" ")
        # print(rr)
        data.append([rr[1], int(rr[3])])
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
    data = Read_Data("pumsb_0.7.csv")  # 取出的是频繁项集的名称
    data_c = sorted(data, key=lambda x: int(x[1]), reverse=True)
    data_c_50 = []
    for dd in data_c[:100]:
        data_c_50.append(dd[0])

    # print(data_c_50)
    F_sum = 0
    Re_sum = 0
    for i in range(1, 11):

        noise_data_read = 'pumsb_0.7_noise_' + str(i) + '.csv'
        noise_data, re = Read_noise_Data(noise_data_read)
        noise_c = sorted(noise_data, key=lambda x: int(x[1]), reverse=True)
        noise_c_50 = []

        re_list = []
        for i in range(len(noise_c[: 100])):
            # print(re[i][1], re[i][0])
            re_list.append(abs(float(noise_c[i][2])) / float(noise_c[i][1]))
        median = get_median(re_list)  # median 为相对误差
        Re_error_result.append(median)

        for noise_dd in noise_c[:100]:
            noise_c_50.append(noise_dd[0])
        U = len(set(data_c_50) & set(noise_c_50))
        UP = len(set(noise_c_50))
        UC = len(set(data_c_50))
        precision = U / UP
        recall = U / UC
        F_SCORE = 2 * (precision * recall) / (precision + recall)
        F_Score_result.append(F_SCORE)
    for i in F_Score_result:
        print('fscore:', i)
        F_sum += i
    for j in Re_error_result:
        print('re:', j)
        Re_sum += j
    print('accidents的平均F-Score为：', F_sum/len(F_Score_result))
    print('accidents的平均re为：', Re_sum/len(Re_error_result))

