import xlrd
import matplotlib.pyplot as plt
import numpy as np

# 读取excel类型文件
data = xlrd.open_workbook('train.xlsx')
table = data.sheet_by_index(0)  # 通过索引顺序获取

# table 获取行数、列数
# print(table.nrows)  1593
# print(table.ncols)  266

test = [0] * 266            # 测试集
buckets = [0] * 266         # 训练集

sym = [0] * 10            # 测试数据的类别
count = [0] * 1593        # 平方和
pre = 0                   # 识别精度
y = [0] * 20              # 散点的纵坐标
# 使用二维数组记录测试数据和其他训练数据的欧式距离，[0][t]存储距离，
# 对应的[1][t]存储训练数据数字类别
counts = [[0 for p in range(1593)] for p in range(2)]

# k从1到10
for r in range(1, 21):
    k = r

    # 顺序的把每一行数据作为测试数据
    for p in range(0, 1593):
        test = table.row_values(p)  # 获得第i行数据

        # 计算测试数据与其他训练数据的距离
        for t in range(0, 1593):
            if t == p:
                continue
            buckets = table.row_values(t)

            for i in range(0, 256):
                count[t] += (buckets[i]-test[i])**2

            counts[0][t] = count[t] ** 0.5

            # 识别训练集的类型，0~9
            for j in range(256, 266):
                if buckets[j] == 1:
                    counts[1][t] = j-256
            # [0][t]存储距离，对应的[1][t]存储训练数据数字类别

        # 距离计算结束，找k个最近的
        num = 100    #类型
        mem = 0
        for t in range(0, k):   # 找出k个最邻近的
            m = 10000000000000
            for i in range(0, 1593):
                if i == p:
                    continue
                if counts[0][i] < m:

                    m = counts[0][i]
                    num = counts[1][i]
                    mem = i
            sym[num] += 1
            counts[0][mem] = 1000000  # 找到距离最小的，记录类型后将其设为1000000，下次循环找到第二小的

        # 距离清零，方便下次循环记录
        for i in range(0, 1593):
            count[i] = 0
            counts[0][i] = 0
            counts[1][i] = 10

        temp = [0] * 10
        for t in range(0, 10):
            temp[t] = sym[t]

        # 找出k个最近的当中同一类型最多的那一类，即sym[9]
        # k=2比k=1的错误率低的分析，k=2时sym[9]的值为1或2
        # （1：与样本点最近的两个点的类别不同  2：类别相同）
        # sym[9]=1的情况可能导致k=2比k=1的错误率低
        # 后面实现中定义，两个类别中只要有一个与原类型相同即为识别正确
        sym.sort()

        symbol = 0   # 记录是否正确识别
        for t in range(0, 10):
            if temp[t] == sym[9]:
                for j in range(256, 266):
                    if test[j] == 1:
                        num = j - 256
                if t == num:
                    symbol = 1

        pre = pre + symbol
        for t in range(0, 10):
            sym[t] = 0

    pre = pre / 1593 * 100
    print('k=', k, '  错误率:', 100-pre, '%')
    y[k-1] = 100 - pre
    pre = 0

x = range(1, 21)
plt.plot(x, y)
plt.xlabel('k')
plt.ylabel('%')
plt.show()

