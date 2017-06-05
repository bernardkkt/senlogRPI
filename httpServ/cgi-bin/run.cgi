#!/bin/bash
echo I want to shutdown gracefully.
#mkdir ecc
cd /home/pi/LOGGING
sudo python testsrv.py &
exit
