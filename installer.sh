#!/bin/bash
set -x
set -e

export DEBIAN_FRONTEND="noninteractive"
# This script configures Raspbian to work properly with the sensors.
# Run this script after the fresh installation of Raspbian OS to RPI.
# This script should be working on Raspbian 8 Jessie

mkdir -p /home/pi/LOGGING/
ln -s /home/pi/LOGGING ${PWD}/httpServ/LOGGING

sudo raspi-config nonint do_serial 1
sudo raspi-config nonint do_i2c 0

sudo cp /boot/config.txt /boot/config.txt-bak
echo "enable_uart=1" | sudo tee -a /boot/config.txt
echo "dtparam=i2c_arm_baudrate=8000" | sudo tee -a /boot/config.txt

sudo apt update
sudo apt install xrdp tightvncserver gpsd-clients python-dev libbluetooth-dev -y

gcc -o ipInformer `realpath ${PWD}/ipInformer.c` -lbluetooth
mkdir -p /home/pi/Bluetooth
mv ipInformer /home/pi/Bluetooth/

sudo python -m pip install RPi.GPIO==0.6.2
sudo python -m pip install Adafruit-PureIO==0.2.1
sudo python -m pip install Adafruit-GPIO==1.0.3
sudo python -m pip install Adafruit-BMP==1.5.2

git clone https://bitbucket.org/lunobili/rpisht1x.git /tmp/rpisht1x
sudo python -m pip install /tmp/rpisht1x/src

git clone https://github.com/adamheinrich/gpsdate
cd gpsdate
make all
cd ..

echo "@reboot sudo pigpiod" >> /tmp/crontask
echo "@reboot bash `realpath ${PWD}/startup.sh`" >> /tmp/crontask
crontab /tmp/crontask

sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
sudo systemctl stop ntp
sudo systemctl disable ntp

chmod a+x ${PWD}/httpServ/cgi-bin/*.cgi

echo ""
echo "DONE!"
echo "You may restart your system now."
