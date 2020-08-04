#!/bin/sh

# arg1: scheme name
# arg2: file size arg
# arg3: ec_k
# arg4: ec_m
cp ~/$1-src/*.java /home/hadoop/hadoop-3.1.2-src/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/
cd ~/hadoop-3.1.2-src/
mvn package -Pdist,native -DskipTests -Dtar
cd ~
#for i in $(seq 1 3)
for i in 1
do
echo ${i}
stop-all.sh
#for j in {1..19};do ssh hadoop@n$j "hostname;sudo tc qdisc del dev ens9 root";done
sh ~/backToOrigin.sh
sh ~/putFile.sh 17072 6 3
sleep 25m
sh ~/getFilesLocations.sh 17072 6 3
mkdir $1-LQL${i}
mv allLocationsFile17072M.txt 1.txt
mv 1.txt $1-LQL${i}/
stop-all.sh
#for j in {1..19};do ssh hadoop@n$j "hostname;sudo tc qdisc add dev ens9 root tbf rate 240Mbit latency 50ms burst 15kb";done
sh ~/restart.sh
start-dfs.sh
ssh hadoop@n5 "hdfs --daemon stop datanode"
sleep 22m
sh ~/getFilesLocations.sh 17072 6 3
mv allLocationsFile17072M.txt 2.txt
mv 2.txt $1-LQL${i}/
sh ~/collectLog.sh
mv allLogs.txt $1-LQL${i}/
cp ~/echadoop/hadoop-3.1.2/logs/hadoop-hadoop-namenode-node1.out ~/$1-LQL${i}/hadoop-hadoop-namenode-node1.out
done
