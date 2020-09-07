import csv
import math


def calFileSize(k, m, blockSize, nodeNum, gains, distributeNum):
    stripeNum=math.ceil((nodeNum-1) * gains * nodeNum/(k+m))
    fileSize=stripeNum * k * blockSize

    print("K=",k," ,M=",m," ,blockSize=",blockSize," ,nodeNum=",nodeNum," ,gains=",gains," ,stripeNum=",stripeNum," ,fileSize=",fileSize,"MB", "(", fileSize/1024,"G)", " ,reconSize=", (stripeNum * (k+m) * blockSize)/1024/nodeNum, "G)", " ,genArgs=", math.ceil(fileSize/distributeNum), "MB (", fileSize/distributeNum/1024, "G)")
    print("stripe fileSize:", k * blockSize)
    print("stripe putTimes:", math.ceil(stripeNum/distributeNum))

    return stripeNum,fileSize


if __name__=="__main__":
    erasureCodingPolicy=[(3,2), (6,3), (10,4)]
    times=[50]
    blockSize=16
    distributeNum=17
    DNNums=[17]

    for ecp in erasureCodingPolicy:
        for nn in DNNums:
            for time in times:
                calFileSize(ecp[0], ecp[1], blockSize, nn, time, distributeNum)