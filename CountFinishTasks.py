import re
import datetime
import math


def getTimeCounter(logFile, timeCorrect, diffTime):
    timedic = {}
    f = open(logFile)  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    hostname="null"
    startFlag = "org.apache.hadoop.net.NetworkTopology: Removing a node"
    # startFlag = "LQL Start reconstruction!"
    endFlag="org.apache.hadoop.hdfs.server.datanode.DataNode: Received"
    while line:
        if len(line)<=10 and "node" in line:
            hostname=re.search(r"node\d{1,2}",line).group(0)
            print(hostname)
            if hostname not in timedic:
                timedic[hostname]=[]

        if startFlag in line:
            print(line)
            timestamp=re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2},\d{1,3})", line).group(0)
            timedic[hostname].append(timestamp)

        if endFlag in line:
            print(line)
            timestamp = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2},\d{1,3})", line).group(0)
            timedic[hostname].append(timestamp)

        line = f.readline()

    print(timedic)

    return getTimestampDiff(timedic,timeCorrect,diffTime)


def getTimestampDiff(timedic,timeCorrect,diffTime):
    startDateTime=datetime.datetime.strptime(timedic["node1"][0][:-4], '%Y-%m-%d %H:%M:%S')
    startMicroSecond=int(timedic["node1"][0][-3:])
    # startDateTime=datetime.datetime.strptime("2020-09-18 16:11:35", '%Y-%m-%d %H:%M:%S')
    # startMicroSecond=334

    counterTime={}

    max=-1
    mhostname=""

    for hostname in timedic:
        timestamps=timedic[hostname]
        for ts in timestamps:
            endDateTime=datetime.datetime.strptime(ts[:-4], '%Y-%m-%d %H:%M:%S')
            endMicroSecond=int(ts[-3:])
            diff=(endDateTime-startDateTime).seconds

            # 对集群时间进行修正
            if hostname in timeCorrect:
                diff+=timeCorrect[hostname]

            if diff > 80000:
                continue

            if endMicroSecond>=startMicroSecond:
                diff+=(endMicroSecond-startMicroSecond)/1000
            else:
                diff+=(endMicroSecond-startMicroSecond+1000)/1000-1

            index=math.floor(diff/diffTime)
            if index in counterTime:
                counterTime[index]+=1
            else:
                counterTime[index]=1

            if diff>max:
                max=diff
                print(hostname, " ",max)
                mhostname=hostname
                # if max == 86398.9:
                #     print(hostname)
                #     print(startDateTime)
                #     print(endDateTime)

    ks=sorted(list(counterTime.keys()))

    for key in ks:
        print(key, counterTime[key])

    return counterTime


if __name__=="__main__":
    logFile=r"C:\Users\USTC\Desktop\WBN-LQL1\allLogs.txt"

    # 由于集群时间不同步，因此加入对时间的修正
    timeCorrect={}
    # timeCorrect["node3"]=46

    getTimeCounter(logFile, timeCorrect, 10)