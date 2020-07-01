import re
import csv

class Resulter:

    def __init__(self):
        self.tasksNum=0
        self.allIterateCount=0
        self.successCount=0
        self.sourceGraphMaxflow=[]
        self.destGraphMaxflow=[]
        self.parallelRateArray=[]
        self.ratioArray=[]
        self.randParallelRateArray=[]
        self.randRatioArray=[]


dic={}
f = open(r"F:\Coding\Java\SimulateSR\result\fullbatch-result-K=10-M=4-gains=100.0.txt")  # 返回一个文件对象
line = f.readline()  # 调用文件的 readline()方法
while line:
    info=tuple(re.findall(r"\d+\.?\d*", line))
    dic[info]=Resulter()
    line = f.readline()
    dic[info].tasksNum=re.findall(r"\d+\.?\d*", line)[0]
    line = f.readline()
    dic[info].allIterateCount = re.findall(r"\d+\.?\d*", line)[0]
    line = f.readline()
    dic[info].successCount = re.findall(r"\d+\.?\d*", line)[0]
    line = f.readline()
    dic[info].sourceGraphMaxflow += re.findall(r"\d+\.?\d*", line)
    line = f.readline()
    dic[info].destGraphMaxflow += re.findall(r"\d+\.?\d*", line)
    line = f.readline()
    dic[info].parallelRateArray += re.findall(r"\d+\.?\d*", line)
    line = f.readline()
    dic[info].ratioArray += re.findall(r"\d+\.?\d*", line)

    for i in range(0,5):
        line = f.readline()

    line = f.readline()
    dic[info].randParallelRateArray += re.findall(r"\d+\.?\d*", line)
    line = f.readline()
    dic[info].randRatioArray += re.findall(r"\d+\.?\d*", line)

    line = f.readline()


with open("fullbatch-result-K=10-M=4-gains=100.0.csv","w",encoding="gbk",newline="") as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(["K","M","stripeNum","nodeNum","tasksNum","allIterateCount","successCount","batchNo","sourceGraphMaxflow","destGraphMaxflow","parallelRate","ratio","randParallelRate","randRatio"])

    for key in dic:
        info_list = list(key)
        info_list.append(dic[key].tasksNum)
        info_list.append(dic[key].allIterateCount)
        info_list.append(dic[key].successCount)

        for i in range(int(dic[key].allIterateCount)):
            writer.writerow(info_list+[i, dic[key].sourceGraphMaxflow[i], dic[key].destGraphMaxflow[i],dic[key].parallelRateArray[i],dic[key].ratioArray[i],dic[key].randParallelRateArray[i],dic[key].randRatioArray[i]])