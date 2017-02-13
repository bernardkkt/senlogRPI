#!/bin/bash
function getName {
	currentIP=$(ifconfig wlan | sed -n 's/.*inet addr:\(.*\)Bcast:.*/\1/p')
	nome="DevIP: ${currentIP// }"
	echo "Currently the IP address is: $currentIP"
	if [[ -z "${currentIP// }" ]]; then
		echo "Seems like there's no internet connection at the moment."
		nome="DevIP:N/A"
	fi
	sudo ./ipInformer "$nome"
	echo $nome
	echo
}
echo =========================================
echo "This script detects any changes of the"
echo "system's IP address."
echo =========================================
echo
getName
while true; do
	while [[ $(ifconfig wlan | sed -n 's/.*inet addr:\(.*\)Bcast:.*/\1/p') = $currentIP ]]; do
		sleep 1
		continue
	done
	getName
done
exit 0
