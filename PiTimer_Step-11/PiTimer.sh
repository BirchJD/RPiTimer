#!/bin/bash

# sudo crontab -e
# @boot /home/pi/Desktop/PiTimer/PiTimer_Step-11/PiTimer.sh

cd /home/pi/Desktop/PiTimer/PiTimer_Step-11
sudo python PiTimer.py 

sudo shutdown -h now

