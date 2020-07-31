#!/bin/sh
cp ~/PPR-src/*.java /home/hadoop/hadoop-3.1.2-src/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/
cd ~/hadoop-3.1.2-src/
mvn package -Pdist,native -DskipTests -Dtar
cd ~
for i in $(seq 1 3)
do
echo ${i}
stop-all.sh
~/backToOrigin.sh
~/putFile.sh 15360 3 2
sleep 25m
~/getFilesLocations.sh 15360 3 2
mkdir PPR-LQL${i}
mv allLocationsFile15360M.txt 1.txt
mv 1.txt PPR-LQL${i}/
stop-all.sh
~/restart.sh
start-dfs.sh
ssh hadoop@n5 "hdfs --daemon stop datanode"
sleep 10m
~/getFilesLocations.sh 15360 3 2
mv allLocationsFile15360M.txt 2.txt
mv 2.txt PPR-LQL${i}/
~/collectLog.sh
mv allLogs.txt PPR-LQL${i}/
cp ~/echadoop/hadoop-3.1.2/logs/hadoop-hadoop-namenode-node1.out ~/PPR-LQL${i}/hadoop-hadoop-namenode-node1.out
done
