#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
cd /home/pi/senlogRPI/httpServ
python -m CGIHTTPServer 8080 &
exit
