import re
import csv
import numpy as np


def getBlockLocations(fsckFile,k,m,ipPatten):
    dic = {}
    f = open(fsckFile)  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        info = re.findall(r'(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)', line)
        if len(info) == (k+m+1):
            for i in range(1, (k+m+1)):
                if info[i] in dic:
                    dic[info[i]] += 1
                else:
                    dic[info[i]] = 1

        line = f.readline()

    print(dic)
    print(len(dic))

    for i in range(1, 19):
        if (ipPatten + str(i)) not in dic:
            print(ipPatten + str(i))

    all = 0
    for key in dic:
        all += dic[key]

    print(all)
    return dic


if __name__=="__main__":
    # before = r"C:\Users\Ethen\Desktop\6+3 100\Baseline\06241900-30\1.txt"
    # after = r"C:\Users\Ethen\Desktop\6+3 100\Baseline\06241900-30\2.txt"

    before=r"C:\Users\USTC\Desktop\6+3 100\1.txt"
    after = r"C:\Users\USTC\Desktop\6+3 100\2.txt"

    # before = r"C:\Users\Ethen\Desktop\6+3 100\SlectiveEC\06241730-30\1.txt"
    # after = r"C:\Users\Ethen\Desktop\6+3 100\SlectiveEC\06241730-30\2.txt"

    # dic1 = getBlockLocations(before, 6, 3, ipPatten="192.168.1.")
    # dic2 = getBlockLocations(after, 6, 3, ipPatten="192.168.1.")

    dic1 = getBlockLocations(before, 6, 3, ipPatten = "100.0.0.")
    # dic2 = getBlockLocations(after, 6, 3, ipPatten = "100.0.0.")
    # diffList = []
    # for key in dic2:
    #     diffList.append(dic2[key] - dic1[key])
    #     print(key, " ", dic1[key], " ", dic2[key], " ", dic2[key] - dic1[key])
    #
    # # 求均值
    # arr_mean = np.mean(diffList)
    # # 求方差
    # arr_var = np.var(diffList)
    # # 求标准差
    # arr_std = np.std(diffList, ddof=1)
    # print("平均值为：%f" % arr_mean)
    # print("方差为：%f" % arr_var)
    # print("标准差为:%f" % arr_std)

