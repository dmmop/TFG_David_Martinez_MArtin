#!/bin/bash
printf "\n\nLaunching Hadoop"
printf "\n--------------------------\n\n"
printf "\nStarting DFS system:\n"
$HADOOP_HOME/sbin/start-dfs.sh
printf "\nStarting yarn daemons\n"
$HADOOP_HOME/sbin/start-yarn.sh
printf "\nStarting mapreduce history\n"
$HADOOP_HOME/sbin/mr-jobhistory-daemon.sh start historyserver

printf "\n\nLaunching Apache Spark"
printf "\n--------------------------\n\n"
$SPARK_HOME/sbin/start-all.sh
printf "\n\nLaunching Apache Spark History Server\n"
$SPARK_HOME/sbin/start-history-server.sh
