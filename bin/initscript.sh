#!/bin/bash

export DEBIAN_FRONTEND="noninteractive"
# This script configures Raspbian to work properly with the sensors.
# Run this script after the fresh installation of Raspbian OS to RPI.

cd /home/pi
cp /boot/config.txt tmpp1.txt
echo "enable_uart=1" >> tmpp1.txt
echo "dtparam=i2c_arm_baudrate=8000" >> tmpp1.txt
sudo mv /boot/config.txt /boot/config.txt-bak
sudo mv tmpp1.txt /boot/config.txt
sudo apt update
sudo apt install xrdp tightvncserver gpsd-clients python-dev -y
git clone https://bitbucket.org/lunobili/rpisht1x.git
git clone https://github.com/adafruit/Adafruit_Python_BMP.git
