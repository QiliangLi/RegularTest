import re
import csv

# string="Failure Node: 5"
# # print(re.findall(r"\d+\.?\d*",string))
# # print("Failure Node" in string)

dic={}
f = open(r"F:\Coding\Java\SimulateSR\result\new-result-K=10-M=4-gains=100.0.txt")  # 返回一个文件对象
line = f.readline()  # 调用文件的 readline()方法
while line:
    info=tuple(re.findall(r"\d+\.?\d*", line))
    dic[info]=[]
    line = f.readline()
    if "pass" in line:
        dic[info]+=re.findall(r"\d+\.?\d*", line)
        line = f.readline()
        dic[info]+=re.findall(r"\d+\.?\d*", line)
        line = f.readline()
        dic[info]+=re.findall(r"\d+\.?\d*", line)
        line = f.readline()
        dic[info]+=re.findall(r"\d+\.?\d*", line)
    else:
        line = f.readline()
        dic[info]+=re.findall(r"\d+\.?\d*", line)
        line = f.readline()
        dic[info]+=re.findall(r"\d+\.?\d*", line)
        line = f.readline()
        dic[info]+=re.findall(r"\d+\.?\d*", line)
        line = f.readline()
        dic[info]+=re.findall(r"\d+\.?\d*", line)

    line = f.readline()

with open("new-result-K=10-M=4-gains=100.0.0.csv","w",encoding="gbk",newline="") as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(["K","M","stripeNum","nodeNum","Source MaxFlow","Replace Maxflow","parallelRate","Ratio"])

    for key in dic:
        writer.writerow(list(key)+dic[key])