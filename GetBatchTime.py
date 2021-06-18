import re
import datetime
import matplotlib.pyplot as plt


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


def getMergeDic(d):
    r={}
    for key1 in d:
        for key2 in d[key1]:
            r[key2]=d[key1][key2]

    return r


def getTimeDiff(startDate, startMicro, endDate, endMicro):
    diff=(endDate-startDate).seconds
    if diff > 80000:
        diff=0

    if endMicro>=startMicro:
        diff+=(endMicro-startMicro)/1000
    else:
        diff+=(endMicro-startMicro+1000)/1000-1

    return diff


def plotBatchRecoveryNum(logFile, color, label):
    nnTimestamps, dnReceivingBlkDic, dnReceivedBlkDic=getTimestampsInfo(logFile)

    dnReceivingBlkDic=getMergeDic(dnReceivingBlkDic)
    dnReceivedBlkDic=getMergeDic(dnReceivedBlkDic)
    dnReceivingTimestampDic = getReverseDic(dnReceivingBlkDic)
    dnReceivedTimestampDic = getReverseDic(dnReceivedBlkDic)

    sortedTasks=[(k, dnReceivingTimestampDic[k]) for k in sorted(dnReceivingTimestampDic.keys())]
    startDate=datetime.datetime.strptime(nnTimestamps[0][:-4], '%Y-%m-%d %H:%M:%S')
    startMicro=int(nnTimestamps[0][-3:])
    for i in range(0, len(sortedTasks)):
        blkID=sortedTasks[i][1]
        sd = datetime.datetime.strptime(dnReceivingBlkDic[blkID][:-4], '%Y-%m-%d %H:%M:%S')
        microSd = int(dnReceivingBlkDic[blkID][-3:])
        ed = datetime.datetime.strptime(dnReceivedBlkDic[blkID][:-4], '%Y-%m-%d %H:%M:%S')
        microEd = int(dnReceivedBlkDic[blkID][-3:])

        if i==0:
            plt.plot([getTimeDiff(startDate, startMicro, sd, microSd), getTimeDiff(startDate, startMicro, ed, microEd)], [i,i], color=color, label=label)
        else:
            plt.plot([getTimeDiff(startDate, startMicro, sd, microSd), getTimeDiff(startDate, startMicro, ed, microEd)],
                     [i, i], color=color)

    print(sortedTasks)
    print(len(sortedTasks))


def plotZoomInBatchRecoveryNum(logFile, color, label, startBlkIndex, endBlkIndex):
    nnTimestamps, dnReceivingBlkDic, dnReceivedBlkDic=getTimestampsInfo(logFile)

    dnReceivingBlkDic=getMergeDic(dnReceivingBlkDic)
    dnReceivedBlkDic=getMergeDic(dnReceivedBlkDic)
    dnReceivingTimestampDic = getReverseDic(dnReceivingBlkDic)
    dnReceivedTimestampDic = getReverseDic(dnReceivedBlkDic)

    sortedTasks=[(k, dnReceivingTimestampDic[k]) for k in sorted(dnReceivingTimestampDic.keys())]
    startDate=datetime.datetime.strptime(nnTimestamps[0][:-4], '%Y-%m-%d %H:%M:%S')
    startMicro=int(nnTimestamps[0][-3:])
    for i in range(0, len(sortedTasks)):
        if i>=startBlkIndex and i <=endBlkIndex:
            blkID=sortedTasks[i][1]
            sd = datetime.datetime.strptime(dnReceivingBlkDic[blkID][:-4], '%Y-%m-%d %H:%M:%S')
            microSd = int(dnReceivingBlkDic[blkID][-3:])
            ed = datetime.datetime.strptime(dnReceivedBlkDic[blkID][:-4], '%Y-%m-%d %H:%M:%S')
            microEd = int(dnReceivedBlkDic[blkID][-3:])

            if i == startBlkIndex:
                plt.plot([getTimeDiff(startDate, startMicro, sd, microSd), getTimeDiff(startDate, startMicro, ed, microEd)], [i,i], color=color, label=label)
            else:
                plt.plot(
                    [getTimeDiff(startDate, startMicro, sd, microSd), getTimeDiff(startDate, startMicro, ed, microEd)],
                    [i, i], color)

    print(sortedTasks)
    print(len(sortedTasks))


def setPltZoomIn():
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 15,
             }
    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 14,
             }
    # 设置坐标轴名称
    plt.xlabel('Recovery Time Line (s)', font1)
    plt.ylabel('Task ID', font1)

    # 设置图例
    plt.legend(loc="lower right", prop=font2)

    # 设置坐标刻度字体大小
    # plt.tick_params(labelsize=15)
    plt.yticks(fontproperties='Times New Roman', size=15)
    plt.xticks(fontproperties='Times New Roman', size=15)

    # 设置坐标轴的范围
    plt.axis([85, 175, 400, 600])

    plt.savefig('zoomInEveryTaskRecoveryTime.pdf',bbox_inches='tight',dpi=300,pad_inches=0.0)

    plt.show()


def setPltOrigin():
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 15,
             }
    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 14,
             }
    # 设置坐标轴名称
    plt.xlabel('Recovery Time Line (s)', font1)
    plt.ylabel('Task ID', font1)

    # 设置图例
    plt.legend(loc="lower right", prop=font2)

    # 设置坐标刻度字体大小
    # plt.tick_params(labelsize=15)
    plt.yticks(fontproperties='Times New Roman', size=15)
    plt.xticks(fontproperties='Times New Roman', size=15)

    # 设置坐标轴的范围
    plt.axis([0, 500, 0, 1610])

    plt.savefig('everyTaskRecoveryTime.pdf',bbox_inches='tight',dpi=300,pad_inches=0.0)

    plt.show()


if __name__=="__main__":
    logFile1=r"C:\Users\USTC\Desktop\allLogs-1.txt"
    logFile2=r"C:\Users\USTC\Desktop\allLogs-2.txt"

    # 设置长款比例
    fig, ax = plt.subplots(figsize=(8, 5))
    # plotBatchRecoveryNum(logFile1,"grey", "HDFS")
    # plotBatchRecoveryNum(logFile2,"black", "SelectiveEC")
    # setPltOrigin()

    plotZoomInBatchRecoveryNum(logFile1, "grey", "HDFS", 400, 600)
    plotZoomInBatchRecoveryNum(logFile2, "black", "SelectiveEC", 400, 600)
    setPltZoomIn()

    # x = [[1.1, 2.2], [2, 5]]  # 要连接的两个点的坐标
    # y = [[1, 1], [6, 6]]
    #
    # for i in range(len(x)):
    #     plt.plot(x[i], y[i], color='r')
    #     # plt.scatter(x[i], y[i], color='b')
    #
    # plt.show()