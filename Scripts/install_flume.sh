#!/bin/bash

wget http://apache.rediris.es/flume/1.8.0/apache-flume-1.8.0-bin.tar.gz
tar -xzvf apache-flume-1.8.0-bin.tar.gz
mv apache-flume-1.8.0-bin/ /opt/flume
rm -rf apache-flume-1.8.0-bin.tar.gz
chmod 1777 -R /opt/flume