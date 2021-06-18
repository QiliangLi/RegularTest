import BlockLocation
import ComputeRecoveryTime
import VerifyBlockRecovery
import EveryBatchRecoveryTime
import os

if __name__=="__main__":
    ec_k = 6
    ec_m = 3
    dnNum=17
    blockLocationBefore=r"E:\SelectiveEC材料\异构\1.txt"
    blockLocationAfter= r"E:\SelectiveEC材料\异构\2.txt"
    logPath=r"E:\SelectiveEC材料\异构\allLogs.txt"
    outPath=r"E:\SelectiveEC材料\异构\hadoop-hadoop-namenode-node1.out"

    BlockLocation.main(blockLocationBefore, blockLocationAfter, ec_k, ec_m)
    os.system("pause")
    input()
    ComputeRecoveryTime.main(logPath)
    # EveryBatchRecoveryTime.main(logPath)
    os.system("pause")
    VerifyBlockRecovery.main(logPath, outPath, dnNum)