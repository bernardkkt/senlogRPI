#!/bin/bash

export DEBIAN_FRONTEND="noninteractive"
# This script configures Raspbian to work properly with the sensors.
# Run this script after the fresh installation of Raspbian OS to RPI.
# This script should be working on Raspbian 8 Jessie

cd /home/pi
cp /boot/config.txt tmpp1.txt
echo "enable_uart=1" >> tmpp1.txt
echo "dtparam=i2c_arm_baudrate=8000" >> tmpp1.txt
sudo mv /boot/config.txt /boot/config.txt-bak
sudo mv tmpp1.txt /boot/config.txt

sudo apt update
sudo apt install xrdp tightvncserver gpsd-clients python-dev libbluetooth-dev -y

gcc -o ipInformer `realpath ../src/ipInformer.c` -lbluetooth
mkdir -p /home/pi/Bluetooth
mv ipInformer /home/pi/Bluetooth/

python -m pip install RPi.GPIO
python -m pip install git+https://bitbucket.org/lunobili/rpisht1x.git#subdirectory=src
python -m pip install https://github.com/adafruit/Adafruit_Python_BMP.git

echo "#!/bin/bash" >> runServer.sh
echo "PATH=${PATH}" >> runServer.sh
echo "cd `realpath httpServ`" >> runServer.sh
echo "python -m CGIHTTPServer 8080 &" >> runServer.sh
echo "exit" >> runServer.sh

echo "#!/bin/bash" >> startup.sh
echo "PATH=${PATH}" >> startup.sh
echo "bash `realpath icheckforipchange.sh` &" >> startup.sh
echo "bash `realpath runServer.sh` &" >> startup.sh
echo "bash `realpath runGPS.sh` &" >> startup.sh

echo "@reboot sudo pigpiod" >> /tmp/crontask
echo "@reboot bash `realpath startup.sh`" >> /tmp/crontask
crontab /tmp/crontask

sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
sudo systemctl stop ntp
sudo systemctl disable ntp

echo ""
echo "DONE!"
echo "You may restart your system now."
