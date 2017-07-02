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
	echo "The script cannot proceed to the next step. Please contact \nyour software support team."
	exit
fi
echo Modifying...
cp /etc/rc.local /etc/rc.local.bak
cp /etc/rc.local rc.local
sed -i '$i \sudo bash /home/pi/senlogRPI/startup.sh &' rc.local
