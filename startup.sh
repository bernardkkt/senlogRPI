#!/bin/bash
echo Welcome.
echo This application will insert a timestamp to a file for every execution.
echo 
echo Cheking files...
fname="log.txt"
if [ -e "$fname" ]
then
	echo File exists.
else
	echo File N/A.
	echo Creating new files...
	touch $fname
	echo
fi
echo Retrieving date...
gdate=$(date --iso-8601=seconds)
echo "$gdate"
echo "$gdate" >> log.txt
exit
