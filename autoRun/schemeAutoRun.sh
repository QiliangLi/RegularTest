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
~/backToOrigin.sh
~/putFile.sh $2 $3 $4
sleep 5m
~/getFilesLocations.sh $2 $3 $4
mkdir $1-LQL${i}
mv allLocationsFile$2M.txt 1.txt
mv 1.txt $1-LQL${i}/
stop-all.sh
~/restart.sh
start-dfs.sh
ssh hadoop@n5 "hdfs --daemon stop datanode"
sleep 1000s
~/getFilesLocations.sh $2 $3 $4
mv allLocationsFile$2M.txt 2.txt
mv 2.txt $1-LQL${i}/
~/collectLog.sh
mv allLogs.txt $1-LQL${i}/
cp ~/echadoop/hadoop-3.1.2/logs/hadoop-hadoop-namenode-node1.out ~/$1-LQL${i}/hadoop-hadoop-namenode-node1.out
done
