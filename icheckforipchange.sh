#!/bin/bash
echo =========================================
echo "This script detects any changes of the"
echo "system's IP address."
echo =========================================
currentIP=$(ifconfig wlan | sed -n 's/.*inet addr:\(.*\)Bcast:.*/\1/p')
echo "Currently the IP address is: $currentIP"
while true; do
	until [[ $(ifconfig wlan | sed -n 's/.*inet addr:\(.*\)Bcast:.*/\1/p') = $currentIP ]]; do
	currentIP=$(ifconfig wlan | sed -n 's/.*inet addr:\(.*\)Bcast:.*/\1/p')
	echo "Currently the IP address is: $currentIP"
	done
sleep 1
done
exit 0

