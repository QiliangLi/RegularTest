import re


def getNamenodeResult(rpcResultFile):
    infoDic={}
    f = open(rpcResultFile)  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        if len(line)<=7 and "node" in line:
            break

        if "DatanodeManager-handleHeartbeat-node" in line and "numECTasks" not in line:
            data=re.findall(r'[0-9]+\.?[0-9]*',line)
            if "node"+data[0] not in infoDic:
                infoDic["node"+data[0]]=[]
            infoDic["node"+data[0]]+=data[1:]

        line = f.readline()

    return infoDic


def getDatanodeResult(rpcResultFile):
    infoDic={}
    hostname = ""
    f = open(rpcResultFile)  # 返回一个文件对象
    line = f.readline()  # 调用文件的 readline()方法
    while line:
        if len(line)<=7 and "node" in line:
            hostname = re.search(r"node\d{1,2}", line).group(0)
            if hostname not in infoDic:
                infoDic[hostname]=[]

        if "BPServiceActor-sendHeartBeat-set bpRegistration dnIn dnOut-" in line:
            infoDic[hostname]+=re.findall(r'[0-9]+\.?[0-9]*',line)

        line = f.readline()

    return infoDic


def compareNNDN(rpcResultFile):
    nnInfo=getNamenodeResult(rpcResultFile)
    dnInfo=getDatanodeResult(rpcResultFile)
    for key in nnInfo:
        print(key)
        print(nnInfo[key])
        print(dnInfo[key])


if __name__=="__main__":
    rpcResultFile=r"C:\Users\USTC\Desktop\6+3 100\RPCTest\allOuts.txt"
    compareNNDN(rpcResultFile)
