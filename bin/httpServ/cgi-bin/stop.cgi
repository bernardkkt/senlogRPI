#!/bin/bash
echo I want to terminate the logging task.
#mkdir edd
sudo pkill -e -f testsrv.py
exit
