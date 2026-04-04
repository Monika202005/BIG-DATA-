#!/bin/bash
$HADOOP_HOME/bin/hdfs namenode -format -force 2>/dev/null || true
$HADOOP_HOME/bin/hdfs namenode