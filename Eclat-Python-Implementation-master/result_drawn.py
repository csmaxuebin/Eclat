import matplotlib.pyplot as plt
x = [0.54, 0.58, 0.62, 0.66, 0.7]
x = [0.5, 0.75, 1, 1.25]
x = ['10', '25', '50', '100', '150']

y = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
y = [0, 0.04, 0.08, 0.12, 0.16, 0.2, 0.24, 0.28, 0.32, 0.36, 0.4]
y1 = [0.007, 0.03, 0.08, 0.128, 0.151]
y2 = [0.014, 0.052, 0.115, 0.157, 0.17]
y3 = [0.007, 0.007, 0.008, 0.008, 0.008]

plt.xlabel("k")
# plt.ylabel("F-score")
plt.ylabel("RE")
plt.margins(0, 0)
l1, = plt.plot(x, y1, label='DP-Eclat', marker='o')
l2, = plt.plot(x, y2, color='red',  # 线条颜色
               linewidth=1.0,  # 线条宽度
               label='ST',
               marker='^')  #标签

l3, = plt.plot(x, y3, label='Privbasis', marker='s', linestyle='--')
plt.legend(handles=[l1, l2, l3],  # 使用legend绘制多条曲线
           labels=['Eclat', 'ST', 'Privbasis'],
           loc='best')
plt.savefig('mushroom')
plt.xticks(x)
plt.yticks(y)
plt.show()

# a = [10, 25, 50, 100, 150]
# DP_eclat = [0.96, 0.88, 0.81, 0.7, 0.63]
# ST = [0.8, 0.72, 0.62, 0.52, 0.41]
# Privbasis = [0.69, 0.53, 0.47, 0.39, 0.33]
# bar_width = 0.2  # 设置一个条状图的宽度
# x_14 = list(range(len(a)))
# x_13 = ['10', '25', '50', '100', '150']
# x_15 = [i+bar_width for i in x_14]
# x_16 = [i+bar_width*2 for i in x_14]
# plt.figure(figsize=(8, 5))  # 设置图像大小
# ax = plt.subplot(1, 1, 1)  # 整体图像的位置
# ax.set_xlabel("k")
# ax.set_ylabel("F-Score")
# plt.bar(x_13, DP_eclat, width=bar_width, label="DP-Eclat", color='#c23531')
# plt.bar(x_15, ST, width=bar_width, label="ST", color='#2f4554')
# plt.bar(x_16, Privbasis, width=bar_width, label="Privbasis", color='#547b95')
# plt.legend()
# plt.show()
