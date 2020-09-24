import re
import datetime


def getTimestampsInfo(logFile):
    nnTimestamps=[]
    dnReceivingBlkDic={}
    dnReceivedBlkDic={}
    f = open(logFile)  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    line = f.readline()  # 调用文件的 readline()方法
    startReconveryFlag="LQL Start reconstruction!"
    while line:
        if len(line) <= 10 and "node" in line:
            hostname = re.search(r"node\d{1,2}", line).group(0)
            if hostname not in dnReceivingBlkDic:
                dnReceivingBlkDic[hostname] = dict()
            if hostname not in dnReceivedBlkDic:
                dnReceivedBlkDic[hostname]=dict()

        if startReconveryFlag in line:
            # print(line)
            timestamp = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2},\d{1,3})", line).group(0)
            nnTimestamps.append(timestamp)

        if ("INFO BlockStateChange: BLOCK* neededReconstruction =" in line or "INFO org.apache.hadoop.hdfs.server.blockmanagement.BlockManager: LQL-BLOCK* neededReconstruction" in line) and "neededReconstruction = 0 pendingReconstruction = 0" not in line:
            # print(line)
            timestamp = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2},\d{1,3})", line).group(0)
            nnTimestamps.append(timestamp)

        if "INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Receiving" in line:
            timestamp = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2},\d{1,3})", line).group(0)
            blkID=re.search(r"blk_-\d{19}_\d{4}", line).group(0)
            dnReceivingBlkDic[hostname][blkID]=timestamp

        if "INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Received" in line:
            timestamp = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2},\d{1,3})", line).group(0)
            blkID = re.search(r"blk_-\d{19}_\d{4}", line).group(0)
            dnReceivedBlkDic[hostname][blkID]=timestamp

        line = f.readline()

    return nnTimestamps, dnReceivingBlkDic, dnReceivedBlkDic


def getReverseDic(d):
    r={}
    for key in d:
        r[d[key]+key]=key

    return r


def getBatchRecoveryTime(logFile):
    nnTimestamps, dnReceivingBlkDic, dnReceivedBlkDic=getTimestampsInfo(logFile)
    dnReceivingTimestampDic={}
    dnReceivedTimestampDic={}
    avgTimeList=[]
    maxTimeList=[]

    for hostname in dnReceivingBlkDic:
        dnReceivingTimestampDic[hostname]=getReverseDic(dnReceivingBlkDic[hostname])

    for hostname in dnReceivedBlkDic:
        dnReceivedTimestampDic[hostname]=getReverseDic(dnReceivedBlkDic[hostname])

    for i in range(0,len(nnTimestamps)-1):
        # print(i)
        startTimestamp=nnTimestamps[i]
        endTimestamp=nnTimestamps[i+1]
        batchBlk={}

        for hostname in dnReceivingTimestampDic:
            batchBlk[hostname]=[]
            for t in dnReceivingTimestampDic[hostname]:
                if t >= startTimestamp and t <= endTimestamp:
                    batchBlk[hostname].append(dnReceivingTimestampDic[hostname][t])

        mt=-999
        timeList = []
        for hostname in batchBlk:
            # print(hostname)
            for blkID in batchBlk[hostname]:
                # print(blkID)
                sd=datetime.datetime.strptime(dnReceivingBlkDic[hostname][blkID][:-4], '%Y-%m-%d %H:%M:%S')
                microSd=int(dnReceivingBlkDic[hostname][blkID][-3:])
                ed=datetime.datetime.strptime(dnReceivedBlkDic[hostname][blkID][:-4], '%Y-%m-%d %H:%M:%S')
                microEd = int(dnReceivedBlkDic[hostname][blkID][-3:])

                diff=(ed-sd).seconds
                if diff > 80000:
                    diff=0

                if microEd>=microSd:
                    diff+=(microEd-microSd)/1000
                else:
                    diff+=(microEd-microSd+1000)/1000-1

                print(diff)
                timeList.append(diff)
                if diff>mt:
                    mt=diff

        print("===")
        if len(timeList)!=0:
            avgTimeList.append(sum(timeList)/len(timeList))
        maxTimeList.append(mt)

    print("maxTimeList", maxTimeList)
    print("avgTimeList", avgTimeList)
    print("sum_avgTimeList", sum(avgTimeList))
    return maxTimeList


def getSumRecoveryTime(timeList):
    tmp=0.0
    for t in timeList:
        if t<0:
            continue
        tmp+=t

    print(tmp)
    return tmp


def main(logFile):
    # logFile=r"C:\Users\USTC\Desktop\6+3 100\allLogs.txt"
    maxTimeList=getBatchRecoveryTime(logFile)
    getSumRecoveryTime(maxTimeList)