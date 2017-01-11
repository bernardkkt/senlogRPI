#include <stdio.h>
#include <pigpio.h>

#define sckP 23
#define dtaP 24


void trisSCK(unsigned int pno){
	gpioWrite(pno, 0);
	gpioSetMode(pno, 1);
	gpioWrite(pno, 0);
}

void trisDATA(unsigned int pno){
	gpioSetPullUpDown(pno, 0);
	gpioWrite(pno, 0);
	gpioSetMode(pno, 1);
	gpioSetPullUpDown(pno, 0);
	gpioWrite(pno, 0);
}

int main(int argc, char **argv)
{
	printf("Initialising...\n");
	//Initialisation
	if(gpioInitialise() < 0){
		printf("Cannot proceed. An error has occured.\n");
		return 1;
	}
	trisSCK(sckP);
	trisDATA(dtaP);
	
	//Tasks	
	
	gpioTerminate();
	return 0;
}
