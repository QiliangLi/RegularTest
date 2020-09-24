import re
import csv
import numpy as np


def getBlockLocations(fsckFile,k,m):
    dic = {}
    deadList=[]
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

    for hn in dic.keys():
        deadList.append(hn)
    # print(deadList)

    all = 0
    for key in dic:
        all += dic[key]

    print(all)
    return dic,deadList


def main(blockLocationBefore, blockLocationAfter, ec_k, ec_m):
    # before = r"C:\Users\USTC\Desktop\6+3 100\Baseline\07061900-100-w-sw\1.txt"
    # after = r"C:\Users\USTC\Desktop\6+3 100\Baseline\07061900-100-w-sw\2.txt"

    before = blockLocationBefore
    after = blockLocationAfter

    # before = r"C:\Users\USTC\Desktop\6+3 100\SlectiveEC\07071123-100-16-ns-3\1.txt"
    # after = r"C:\Users\USTC\Desktop\6+3 100\SlectiveEC\07071123-100-16-ns-3\2.txt"

    # dic1 = getBlockLocations(before, 6, 3, ipPatten="192.168.1.")
    # dic2 = getBlockLocations(after, 6, 3, ipPatten="192.168.1.")

    dic1, deadList1 = getBlockLocations(before, ec_k, ec_m)
    dic2, deadList2 = getBlockLocations(after, ec_k, ec_m)

    deadNode=list(set(deadList1).difference(set(deadList2)))
    # print(deadNode)
    print("Dead node:")
    reconBlkSum=0
    for dn in deadNode:
        reconBlkSum+=dic1[dn]
        print(dn, dic1[dn])
    print("reconBlkSum: ",reconBlkSum)

    diffList = []
    for key in dic2:
        diffList.append(dic2[key] - dic1[key])
        print(key, " ", dic1[key], " ", dic2[key], " ", dic2[key] - dic1[key])

    # 求均值
    arr_mean = np.mean(diffList)
    # 求方差
    arr_var = np.var(diffList)
    # 求标准差
    arr_std = np.std(diffList, ddof=1)
    print("平均值为：%f" % arr_mean)
    print("方差为：%f" % arr_var)
    print("标准差为:%f" % arr_std)

