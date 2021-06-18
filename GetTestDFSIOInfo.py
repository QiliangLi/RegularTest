import re
import csv


def getTestDFSIOInfo(logPath, recordEntries):
    f = open(logPath)  # 返回一个文件对象
    line = f.readline()
    writeThgpt=[]
    writeExecTime=[]
    readThgpt=[]
    readExecTime=[]
    find_float = lambda x: re.search("\d+(\.\d+)?", x).group()

    while line:
        if "----- TestDFSIO -----" in line and "write" in line:
            line = f.readline()
            line = f.readline()
            line = f.readline()
            line = f.readline()
            writeThgpt.append(float(find_float(line)))
            line = f.readline()
            line = f.readline()
            line = f.readline()
            writeExecTime.append(float(find_float(line)))

        if "----- TestDFSIO -----" in line and "read" in line:
            line = f.readline()
            line = f.readline()
            line = f.readline()
            line = f.readline()
            readThgpt.append(float(find_float(line)))
            line = f.readline()
            line = f.readline()
            line = f.readline()
            readExecTime.append(float(find_float(line)))

        line = f.readline()

    # print("writeThgpt: ", writeThgpt[-recordEntries:])
    # print("readThgpt: ", readThgpt[-recordEntries:])
    # print("writeExecTime: ", writeExecTime[-recordEntries:])
    # print("readExecTime: ", readExecTime[-recordEntries:])

    writeThgpt=writeThgpt[-recordEntries:]
    readThgpt=readThgpt[-recordEntries:]
    writeExecTime=writeExecTime[-recordEntries:]
    readExecTime=readExecTime[-recordEntries:]

    half=int(recordEntries/2)
    print("writeThgpt:")
    print(writeThgpt[:half])
    print(writeThgpt[half:])

    # print("readThgpt:")
    # print(readThgpt[:half])
    # print(readThgpt[half:])

    print("writeExecTime:")
    print(writeExecTime[:half])
    print(writeExecTime[half:])

    # print("readExecTime:")
    # print(readExecTime[:half])
    # print(readExecTime[half:])


if __name__=="__main__":
    logPath=r"E:\SelectiveEC材料\异构\TestDFSIO_results.log"
    recordEntries=30
    getTestDFSIOInfo(logPath, recordEntries)