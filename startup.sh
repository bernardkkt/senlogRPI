#!/bin/bash
echo
echo Logging application starting up...
echo
echo Retrieving real time from GPS...
gmode=$(gpspipe -w | head -4 | egrep -o '"mode":+[0-9]' | grep -Po  '"mode":\K[^ ]+')
while [ "$gmode" = "1" ]; do
	echo Still attempting...
	gmode=$(gpspipe -w | head -4 | egrep -o '"mode":+[0-9]' | grep -Po  '"mode":\K[^ ]+')
	sleep 1
done
echo Changing system time...
sudo killall gpsd
sudo ./gpsdate /dev/ttyS0
echo
echo Success!
sudo gpsd /dev/ttyS0 -n
echo The script will now proceed to logging task.
cd LOGGING
sudo python mainlog.py
