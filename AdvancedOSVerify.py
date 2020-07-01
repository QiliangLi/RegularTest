import os

def getStandard(file):
    f = open(file)  # 返回一个文件对象
    line = f.readline()
    standard=[]
    while line:
        standard.append(int(line))
        line = f.readline()

    return standard


def getComputeResult(rootPath):
    files=os.listdir(rootPath)
    computeResult = []
    for file in files:
        print(os.path.join(rootPath,file))
        f = open(os.path.join(rootPath,file))  # 返回一个文件对象
        line = f.readline()

        while line:
            computeResult.append(int(line))
            line = f.readline()

    return computeResult


if __name__=="__main__":
    rootPath=r"C:\Users\Ethen\Desktop\高操大作业jar\LTest\output\Rec"
    standardFile=r"F:\第一题数据集\第一题数据集\测试样本\result.txt"

    computeResult=getComputeResult(rootPath)
    standard=getStandard(standardFile)

    counter=0

    for i in range(0,len(computeResult)):
        if computeResult[i]==standard[i]:
            counter+=1

    print(counter,len(computeResult),counter/len(computeResult))