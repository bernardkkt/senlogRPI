#!/bin/bash
sudo pkill -e -f logger.py &
echo "Content-Type: text/html"
echo
echo "<html><head><meta http-equiv=\"Refresh\" content=\"5;url=./../cmd.html\"></head>"
echo "<body><p>"
echo "The logging application is stopping. You will be navigated to the previous page..."
echo "</p></body></html>"
exit
