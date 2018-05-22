#!/bin/bash
printf "\n\nStoping Hadoop"
printf "\n--------------------------\n\n"
printf "\nStoping DFS system\n"
$HADOOP_HOME/sbin/stop-dfs.sh
printf "\nStoping yarn daemons\n"
$HADOOP_HOME/sbin/stop-yarn.sh
printf "\nStoping mapreduce history server\n"
$HADOOP_HOME/sbin/mr-jobhistory-daemon.sh stop historyserver

printf "\n\nStoping Apache Spark"
printf "\n--------------------------\n\n"
$SPARK_HOME/sbin/stop-all.sh
printf "\n\nStoping Apache Spark History Server\n"
$SPARK_HOME/sbin/stop-history-server.sh