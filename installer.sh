#!/bin/bash
cd /home/ubuntu
#cd /home/pi
echo -e "Welcome.\n"
echo -e "This script will set up the system for the data logging \nsoftware to work.\n"
echo -e "Checking file's integrity..."
if [ "`tail -n1 /etc/rc.local`" = "exit 0" ]
then
	echo -e "The script is ready to proceed."
else
	echo -e "The script cannot proceed to the next step. Please contact \nyour software support team."
	exit
fi
echo Modifying...
sudo cp /etc/rc.local /etc/rc.local.bak
cp /etc/rc.local rc.local
sed -i '$i \sudo bash /home/pi/senlogRPI/startup.sh &' rc.local
sudo mv -f rc.local /etc/rc.local
echo Compiling executable...
sudo apt-get install libbluetooth-dev -y
gcc senlogRPI/ipInformer.c -lbluetooth -o senlogRPI/ipInformer
if [ -e senlogRPI/ipInformer ]
then
	echo -e "Blutooth name changing utility is now ready."
else
	echo -e "Error: Unable to create executable file. Please contact \nyour software support team."
	exit
fi
echo Exiting...
