#!/bin/bash

screen -dmS flume flume-ng agent --conf /opt/flume/conf --conf-file /home/david/Desktop/David_Martinez_Martin/Conf_Files/Flume-TwitterAgent.conf --name TwitterAgent -Dflume.root.logger=INFO,console


