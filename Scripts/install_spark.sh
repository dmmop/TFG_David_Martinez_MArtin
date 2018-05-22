#!/bin/bash

cd /opt
wget http://apache.uvigo.es/spark/spark-2.2.0/spark-2.2.0-bin-hadoop2.7.tgz
tar -xvzf spark-2.2.0-bin-hadoop2.7.tgz 
mv spark-2.2.0-bin-hadoop2.7 spark
rm -rf spark-2.2.0-bin-hadoop2.7.tgz
chmod 1777 -R /opt/spark