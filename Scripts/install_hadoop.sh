#!/bin/bash

wget http://www-us.apache.org/dist/hadoop/common/stable2/hadoop-2.9.0.tar.gz
tar -xzvf hadoop-2.9.0.tar.gz
mv hadoop-2.9.0/ /opt/hadoop
rm -rf hadoop-2.9.0.tar.gz
chmod 1777 -R /opt/hadoop