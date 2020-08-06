#!/bin/sh
cd /home/qingya/hadoop-3.1.2-src/hadoop-hdfs-project/hadoop-hdfs-client
mvn package -Pdist -Dtar -DskipTests
cp /home/qingya/hadoop-3.1.2-src/hadoop-hdfs-project/hadoop-hdfs-client/target/hadoop-hdfs-client-3.1.2.jar /home/qingya/compile

cd /home/qingya/hadoop-3.1.2-src/hadoop-mapreduce-project/hadoop-mapreduce-client/hadoop-mapreduce-client-core
mvn package -Pdist -Dtar -DskipTests
cp /home/qingya/hadoop-3.1.2-src/hadoop-mapreduce-project/hadoop-mapreduce-client/hadoop-mapreduce-client-core/target/hadoop-mapreduce-client-core-3.1.2.jar /home/qingya/compile

cd /home/qingya/hadoop-3.1.2-src/hadoop-common-project/hadoop-common
mvn package -Pdist -Dtar -DskipTests
cp /home/qingya/hadoop-3.1.2-src/hadoop-common-project/hadoop-common/target/hadoop-common-3.1.2.jar /home/qingya/compile
