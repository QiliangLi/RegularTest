import BlockLocation
import ComputeRecoveryTime
import VerifyBlockRecovery
import os

if __name__=="__main__":
    ec_k = 3
    ec_m = 2
    dnNum=17
    blockLocationBefore=r"C:\Users\USTC\Desktop\6+3 100\1.txt"
    blockLocationAfter= r"C:\Users\USTC\Desktop\6+3 100\2.txt"
    logPath=r"C:\Users\USTC\Desktop\6+3 100\allLogs.txt"
    outPath=r"C:\Users\USTC\Desktop\6+3 100\hadoop-hadoop-namenode-node1.out"

    BlockLocation.main(blockLocationBefore, blockLocationAfter, ec_k, ec_m)
    os.system("pause")
    input()
    ComputeRecoveryTime.main(logPath)
    os.system("pause")
    VerifyBlockRecovery.main(logPath, outPath, dnNum)