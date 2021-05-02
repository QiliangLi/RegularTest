import BlockLocation
import ComputeRecoveryTime
import VerifyBlockRecovery
import EveryBatchRecoveryTime
import os

if __name__=="__main__":
    ec_k = 6
    ec_m = 3
    dnNum=17
    blockLocationBefore=r"C:\Users\USTC\Desktop\WBO-LQL1\1.txt"
    blockLocationAfter= r"C:\Users\USTC\Desktop\WBO-LQL1\2.txt"
    logPath=r"C:\Users\USTC\Desktop\WBO-LQL1\allLogs.txt"
    outPath=r"C:\Users\USTC\Desktop\WBO-LQL1\hadoop-hadoop-namenode-node1.out"

    BlockLocation.main(blockLocationBefore, blockLocationAfter, ec_k, ec_m)
    os.system("pause")
    input()
    ComputeRecoveryTime.main(logPath)
    # EveryBatchRecoveryTime.main(logPath)
    os.system("pause")
    VerifyBlockRecovery.main(logPath, outPath, dnNum)