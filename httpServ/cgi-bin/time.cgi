#!/bin/bash
echo "Content-Type: text/html"
echo
echo "<html><head><meta charset=\"UTF-8\"></head>"
echo "<body><p>You should see a timestamp under 'Updating time' if the system time is successfully updated.</p><h1>Current system time...</h1><p>"
date
echo "<body><h1>Updating time...</h1><p>"
sudo rdate time.nist.gov
echo "</p></body></html>"
exit