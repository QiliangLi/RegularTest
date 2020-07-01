import csv
import math


def calFileSize(k, m, blockSize, nodeNum, gains):
    stripeNum=math.ceil((nodeNum-1) * gains * nodeNum/(k+m))
    fileSize=stripeNum * k * blockSize

    print("K=",k," ,M=",m," ,blockSize=",blockSize," ,nodeNum=",nodeNum," ,gains=",gains," ,stripeNum=",stripeNum," ,fileSize=",fileSize,"MB")
    return stripeNum,fileSize


if __name__=="__main__":
    erasureCodingPolicy=[(3,2), (6,3), (10,4)]
    times=[30]
    blockSize=32
    nodeNums=[18]

    for ecp in erasureCodingPolicy:
        for nn in nodeNums:
            for time in times:
                calFileSize(ecp[0], ecp[1], blockSize, nn, time)