import re
import csv


hostname2IP={}
# hostname2IP["node2"]="192.168.1.12"
# hostname2IP["node3"]="192.168.1.13"
# hostname2IP["node4"]="192.168.1.14"
# hostname2IP["node5"]="192.168.1.15"
# hostname2IP["node6"]="192.168.1.16"
# hostname2IP["node7"]="192.168.1.17"
# hostname2IP["node8"]="192.168.1.18"
# hostname2IP["node9"]="192.168.1.19"
# hostname2IP["node10"]="192.168.1.20"
# hostname2IP["node11"]="192.168.1.21"
# hostname2IP["node12"]="192.168.1.22"
# hostname2IP["node13"]="192.168.1.23"
# hostname2IP["node14"]="192.168.1.24"
# hostname2IP["node15"]="192.168.1.25"
# hostname2IP["node16"]="192.168.1.26"
# hostname2IP["node17"]="192.168.1.27"
# hostname2IP["node18"]="192.168.1.28"
# hostname2IP["node19"]="192.168.1.29"

hostname2IP["node2"]="100.0.0.2"
hostname2IP["node3"]="100.0.0.3"
hostname2IP["node4"]="100.0.0.4"
hostname2IP["node5"]="100.0.0.5"
hostname2IP["node6"]="100.0.0.6"
hostname2IP["node7"]="100.0.0.7"
hostname2IP["node8"]="100.0.0.8"
hostname2IP["node10"]="100.0.0.9"
hostname2IP["node11"]="100.0.0.10"
hostname2IP["node12"]="100.0.0.11"
hostname2IP["node13"]="100.0.0.12"
hostname2IP["node14"]="100.0.0.13"
hostname2IP["node15"]="100.0.0.14"
hostname2IP["node16"]="100.0.0.15"
hostname2IP["node17"]="100.0.0.16"
hostname2IP["node18"]="100.0.0.17"
hostname2IP["node19"]="100.0.0.18"


def verifyNNOut(outFile):
    print("Starting verify outfile...")
    rw2target={}
    rw2IP={}
    cpRw=[]
    sendRw=[]
    f = open(outFile)  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    LQLblkId=""
    recoverblkId=""
    while line:
        if "LQL-Send rw:" in line:
            LQLblkId=re.search(r"blk_-\d{19}_\d{4}", line).group(0)
            cpRw.append(LQLblkId)
            if LQLblkId not in rw2target:
                rw2target[LQLblkId]=[]

        if "rw.Targets:" in line:
            tgtNode=re.search(r"node\d{1,2}",line).group(0)
            rw2target[LQLblkId].append(tgtNode)

        if "Recovering BP-" in line:
            recoverblkId = re.search(r"blk_-\d{19}_\d{4}", line).group(0)
            ips=re.findall(r'(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)', line)
            sendRw.append(recoverblkId)
            if recoverblkId not in rw2IP:
                rw2IP[recoverblkId]=[]
            rw2IP[recoverblkId].append(ips[-1])

        line = f.readline()

    for id in cpRw:
        if sendRw.count(id)!=1:
            print(id, " ", sendRw.count(id))

    print("+++++++++++++++++++++++++++++++++++++")

    for blkId in rw2target:
        if blkId not in rw2IP:
            print(blkId, rw2target[blkId])
            continue

        if len(rw2target[blkId])!=len(rw2IP[blkId]):
            print(blkId, rw2target[blkId], rw2IP[blkId])
            continue

        for i in range(len(rw2target[blkId])):
            if hostname2IP.get(rw2target[blkId][i])!=rw2IP[blkId][i]:
                print(blkId, rw2target[blkId], rw2IP[blkId])
                break

    print("Outfile verify complete!=================================================")


def verifyLogs(logFile):
    failureDic={}
    print("Starting verify logfile...")
    cpRw = []
    finishRw = []
    hostname = "null"
    counter=0
    f = open(logFile)  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        if len(line)<=10 and "node" in line:
            hostname=re.search(r"node\d{1,2}",line).group(0)
            if hostname not in failureDic:
                failureDic[hostname]=0

        if "LQL-BLOCK* ask" in line:
            cpRw.append(re.search(r"blk_-\d{19}_\d{4}", line).group(0))

        if "INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Received BP" in line:
            finishRw.append(re.search(r"blk_-\d{19}_\d{4}", line).group(0))

        if "java.io.IOException: Transfer failed for all targets" in line:
            failureDic[hostname]+=1
            counter+=1

        line = f.readline()

    for id in cpRw:
        if finishRw.count(id) != 1:
            print(id, " ", finishRw.count(id))

    print(len(cpRw))
    print(len(set(cpRw)))
    print(cpRw)
    print(len(finishRw))
    print(len(set(finishRw)))
    print(finishRw)

    print(failureDic)
    print(counter)

    print("Logfile verify complete!=================================================")


def findStrInFile(file, ts):
    counter=0
    f = open(file)  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        if ts in line:
            counter+=1

        line = f.readline()

    return counter


def verifyRwIndex(file, nodeNum):
    print("Verify rw index==========================================")
    indexes=[]
    batchSize=nodeNum-1
    f=open(file)
    line=f.readline()
    counter=0
    while line:
        if "Send to DNs reconWorkMap" in line:
            subindexes=re.findall(r"\d+",line)
            for i in range(1,len(subindexes),2):
                indexes.append(subindexes[i])

            if len(set(indexes))!=len(indexes):
                counter+=1
                print(line)

        line = f.readline()

    print(counter)


def verifyComputeTargets(file):
    print("Verify rw targets==========================================")
    targetsCounter={}
    f = open(file)
    line = f.readline()
    counter=0
    while line:
        if "rw.Targets:" in line:
            hostname = re.search(r"node\d{1,2}", line).group(0)
            if hostname not in targetsCounter:
                targetsCounter[hostname]=0

            targetsCounter[hostname]+=1

        line = f.readline()

    for hn in targetsCounter:
        counter+=targetsCounter[hn]
        print(hostname2IP[hn], targetsCounter[hn])

    print(counter)


def verifyDestMapper(file,nodeNum):
    print("Verify destMapper==========================================")
    f = open(file)
    line = f.readline()
    destCounter={}
    while line:
        if "destMapper" in line:
            batchSize=nodeNum-1
            while(batchSize>0):
                line = f.readline()
                # print(line)
                id=re.search(r"\d+", line).group(0)
                if id not in destCounter:
                    destCounter[id]=0
                destCounter[id]+=1
                batchSize-=1

        line = f.readline()

    for id in destCounter:
        print(id, destCounter[id])


def getTasksSizeBeforeTimeout(file):
    f = open(file)  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    flag=True
    beforeTimeoutCounter=0
    timeoutCounter=0
    while line:
        if flag==True:
            if "BLOCK* ask" in line:
                beforeTimeoutCounter+=1

        if "PendingReconstructionMonitor timed out blk_" in line:
            timeoutCounter+=1
            flag=False

        line = f.readline()

    print("beforeTimeoutCounter:",beforeTimeoutCounter)
    print("timeoutCounter:",timeoutCounter)


def getComputeTime(file):
    f = open(file)  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        if "Compute time: " in line or "Compute time include sleep: " in line:
            print(line)

        if "pprComputeTime" in line or "carComputeTime" in line:
            print(line)

        line = f.readline()


def main(logPath, outPath, dnNum):
    # outFile=r"C:\Users\Ethen\Desktop\NotIntegerBatch\logs\hadoop-hadoop-namenode-node1.out"
    # logFile=r"C:\Users\Ethen\Desktop\NotIntegerBatch\allLogs.txt"

    outFile = outPath
    logFile = logPath

    # outFile = r"C:\Users\USTC\Desktop\6+3 100\Baseline\07061900-100-w-sw\hadoop-hadoop-namenode-node1.out"
    # logFile = r"C:\Users\USTC\Desktop\6+3 100\Baseline\07061900-100-w-sw\allLogs.txt"

    verifyNNOut(outFile)
    verifyLogs(logFile)

    print("crgMaxflow:", findStrInFile(outFile, "crgMaxflow:"))
    print("full crgMaxflow:", findStrInFile(outFile, "crgMaxflow: 16"))
    print("rw.Targets:", findStrInFile(outFile, "rw.Targets:"))
    print("LQL-BLOCK*", findStrInFile(logFile, "LQL-BLOCK*"))
    print("Failed to place enough replicas:", findStrInFile(logFile, "Failed to place enough replicas"))
    print("Not enough replicas was chosen:", findStrInFile(logFile, "Not enough replicas was chosen"))
    print("Deleted:", findStrInFile(logFile, "Deleted"))

    verifyRwIndex(outFile, dnNum)
    verifyComputeTargets(outFile)
    verifyDestMapper(outFile, dnNum)
    getTasksSizeBeforeTimeout(logFile)
    getComputeTime(outFile)
