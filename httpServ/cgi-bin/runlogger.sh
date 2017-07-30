#!/bin/bash
cd /home/pi/LOGGING
sudo python logger.py > debug.txt
sudo rm debug.txt
exit
