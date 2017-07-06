#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
echo
echo Logging application starting up...
echo
echo Retrieving real time from GPS...
gmode=$(gpspipe -w -n 5 | sed -n -e 's/.*mode":\(.*\),"time.*/\1/p' | sed -n 1p)
until [[ "$gmode" = "2" ]] || [[ "$gmode" = "3" ]]; do
	echo Still attempting...
	gmode=$(gpspipe -w -n 5 | sed -n -e 's/.*mode":\(.*\),"time.*/\1/p' | sed -n 1p)
	sleep 1
done
echo Changing system time...
sudo killall gpsd
sudo /home/pi/gpsdate/gpsdate /dev/ttyS0
echo
echo Success!
sudo gpsd /dev/ttyS0 -n
echo The script will now proceed to logging task.
cd /home/pi/LOGGING
sudo python logger.py
