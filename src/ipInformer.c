// Compile with -lbluetooth parameter.
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <linux/socket.h>
#include <linux/ioctl.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/hci_lib.h>

int main(int argc, char **argv)
{
	if(argc != 2) {
		printf("Usage: ipInformer \"[ name (without bracket)]\"\n");
		exit(1);
	}
    int dev_id, sock;

    dev_id = hci_get_route(NULL);
    sock = hci_open_dev( dev_id );
    if (dev_id < 0 || sock < 0) {
        perror("opening socket");
        exit(1);
    }

    const char *nome = argv[1];
    hci_write_local_name(sock, nome, 0);
    //Code above might be equivalent to "hci_write_local_name(sock, argv[1], 0);"
    //Codes referred from hciconfig.c
    ioctl(sock, HCIDEVDOWN, dev_id);
    ioctl(sock, HCIDEVUP, dev_id);
    struct hci_dev_req dr;
    dr.dev_id  = dev_id;
    dr.dev_opt = SCAN_DISABLED;
    dr.dev_opt = SCAN_PAGE | SCAN_INQUIRY;
    ioctl(sock, HCISETSCAN, (unsigned long) &dr);
    printf("Good to go.\n");

    close( sock );    
    return 0;
}
