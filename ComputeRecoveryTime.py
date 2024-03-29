import re
import datetime


def getRecoveryTime(logFile,timeCorrect):
    timedic = {}
    f = open(logFile)  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    hostname="null"
    startFlag = "org.apache.hadoop.net.NetworkTopology: Removing a node"
    # startFlag = "LQL Start reconstruction!"
    endFlag="org.apache.hadoop.hdfs.server.datanode.DataNode: Received"
    helpFlag="of size 134217728"
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

        if endFlag in line and helpFlag in line:
        # if endFlag in line:
            print(line)
            timestamp = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2},\d{1,3})", line).group(0)
            timedic[hostname].append(timestamp)

        line = f.readline()

    print(timedic)

    return getTimestampDiff(timedic,timeCorrect)


def getTimestampDiff(timedic,timeCorrect):
    startDateTime=datetime.datetime.strptime(timedic["node1"][0][:-4], '%Y-%m-%d %H:%M:%S')
    startMicroSecond=int(timedic["node1"][0][-3:])
    # startDateTime=datetime.datetime.strptime("2020-09-18 16:11:35", '%Y-%m-%d %H:%M:%S')
    # startMicroSecond=334

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

            if diff>max:
                max=diff
                print(hostname, " ",max)
                mhostname=hostname
                # if max == 86398.9:
                #     print(hostname)
                #     print(startDateTime)
                #     print(endDateTime)

    print(mhostname)
    return max


def main(logPath):
    logFile=logPath
    # logFile=r"C:\Users\USTC\Desktop\6+3 100\SlectiveEC\07032056-100\allLogs.txt"
    # logFile=r"C:\Users\Ethen\Desktop\6+3 100\Baseline\06182200\allLogs.txt"

    # 由于集群时间不同步，因此加入对时间的修正
    timeCorrect={}
    # timeCorrect["node3"]=46

    max=getRecoveryTime(logFile,timeCorrect)
    print("Max: ", max, "seconds", max/60, "min")




# content="2020-06-04 12:43:31,124 INFO org.apache.hadoop.net.NetworkTopology: Removing a node: /default-rack/192.168.1.18:9866"
# startFlag="org.apache.hadoop.net.NetworkTopology: Removing a node"
#
# print(len("node1"))
#
# result=content.find(startFlag)!=-1
# print(result)
# result=startFlag in content
# print(result)
#
# host="node10,node2"
# hn=re.search(r"node\d{1,2}",host)
# print(hn.group(0))
#
# mat = re.search(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2}:\d{1,2},\d{1,3})",content)
# print(mat.group(0))

# print(re.findall(r"\d+\.?\d*",'2020-06-08 23:14:54,095'))
# d1 = datetime.datetime.strptime('2012-03-02 17:42:35,200', '%Y-%m-%d %H:%M:%S,%f')
# d2 = datetime.datetime.strptime('2012-03-02 17:41:20,100', '%Y-%m-%d %H:%M:%S,%f')
# delta = d1 - d2
# print(delta.seconds)
# delta = d2 - d1
# print(delta.seconds)

# s='2012-03-02 17:42:35,200'
# print(s[:-4])