#include <stdio.h>
#include <pigpio.h>

unsigned char SHT1x_crc;
unsigned char SHT1x_status_reg = 0;

#define sckP 23
#define dtaP 24
#define SHT1x_SCK_HI gpioWrite(sckP, 1)
#define SHT1x_SCK_LO gpioWrite(sckP, 0)
#define SHT1x_DATA_LO gpioWrite(dtaP, 0);gpioSetMode(dtaP, 1)
#define	SHT1x_DATA_HI gpioSetMode(dtaP, 0)

void trisSCK(void){
	gpioWrite(sckP, 0);
	gpioSetMode(sckP, 1);
	gpioWrite(sckP, 0);
}

void trisDATA(void){
	gpioSetPullUpDown(dtaP, 0);
	gpioWrite(dtaP, 0);
	gpioSetMode(dtaP, 1);
	gpioSetPullUpDown(dtaP, 0);
	gpioWrite(dtaP, 0);
}

unsigned char SHT1x_Mirrorbyte(unsigned char value){
	unsigned char ret=0, i;
	for (i = 0x80; i; i >>= 1)
	{
		if(value & 0x01)
			ret |= i;
		value >>= 1;
	}
	return ret;
}

void startTransmission(void){
  gpioWrite(sckP, 1);
  gpioDelay(2);
  gpioWrite(dtaP, 0);
  gpioSetMode(dtaP, 1);
  gpioDelay(2);

  gpioWrite(sckP, 0);
  gpioDelay(2);
  gpioWrite(sckP, 1);
  gpioDelay(2);

  gpioSetMode(dtaP, 0);
  gpioDelay(2);
  gpioWrite(sckP, 0);
  gpioDelay(2);

  SHT1x_crc = SHT1x_Mirrorbyte(SHT1x_status_reg & 0x0F);
}

void SHT1x_Crc_Check(unsigned char value){
  unsigned char i;
  for(i = 8; i; i--){
    if ((SHT1x_crc ^ value) & 0x80){
			SHT1x_crc <<= 1;
			SHT1x_crc ^= 0x31;
		}
		else SHT1x_crc <<= 1;
		value <<=1;
  }
}

unsigned char SHT1x_Sendbyte(unsigned char value){
  unsigned char mask;
	unsigned char ack;

  for(mask = 0x80; mask; mask >>= 1){
		gpioWrite(sckP, 0);
    gpioDelay(2);
		if(value & mask){
			gpioSetMode(dtaP, 0);
      gpioDelay(2);
		}
		else{
			gpioWrite(dtaP, 0);
      gpioSetMode(dtaP, 1);
      gpioDelay(2);
		}
		gpioWrite(sckP, 1);
    gpioDelay(2);
	}
  gpioWrite(sckP, 0);
  gpioDelay(2);

  gpioSetMode(dtaP, 0);
  gpioDelay(2);
  gpioWrite(sckP, 1);
  gpioDelay(2);

  ack = 0;
  if(!gpioRead(sckP)) ack = 1;

  gpioWrite(sckP, 0);
  gpioDelay(2);
  //SHT1x_Crc_Check(value);
  return ack;
}

void SHT1x_Reset(void){
  gpioSetMode(dtaP, 0);
  gpioDelay(2);
  int i;
  for(i = 0; i < 9; i++){
    gpioWrite(sckP, 1);
    gpioDelay(2);
    gpioWrite(sckP, 0);
    gpioDelay(2);
  }
  startTransmission();
  SHT1x_Sendbyte(0x1E);
}

int main(int argc, char **argv){
	printf("Initialising...\n");
	//Initialisation
	if(gpioInitialise() < 0){
		printf("Cannot proceed. An error has occured.\n");
		return 1;
	}
	trisSCK();
	trisDATA();
	SHT1x_Reset();

	//Tasks

	gpioTerminate();
	return 0;
}
