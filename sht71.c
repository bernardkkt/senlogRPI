#include <stdio.h>
#include <pigpio.h>

#define sckP 23
#define dtaP 24
#define SHT1x_SCK_HI gpioWrite(sckP, 1)
#define SHT1x_SCK_LO gpioWrite(sckP, 0)
#define SHT1x_DATA_LO gpioWrite(dtaP, 0);gpioSetMode(dtaP, 1)
#define	SHT1x_DATA_HI gpioSetMode(dtaP, 0)
#define SHT1x_GET_BIT gpioRead(dtaP)

unsigned char SHT1x_crc, tHibyte, tLobyte;
unsigned char SHT1x_status_reg = 0;

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
	if(!gpioRead(dtaP)) ack = 1;
	
	gpioWrite(sckP, 0);
	gpioDelay(2);
	SHT1x_Crc_Check(value);
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

unsigned char SHT1x_Measure_Start(unsigned char value){
	startTransmission();
	return SHT1x_Sendbyte(value);
}

unsigned char SHT1x_Readbyte(unsigned char send_ack){
	unsigned char mask;
	unsigned char value = 0;

	for(mask=0x80; mask; mask >>= 1){
		gpioWrite(sckP, 1);
		gpioDelay(2);  	// SCK hi
		if(gpioRead(dtaP) != 0) value |= mask;
		gpioWrite(sckP, 0);
		gpioDelay(2);
	}

	if(send_ack){
		gpioWrite(dtaP, 0);
		gpioSetMode(dtaP, 1);
		gpioDelay(2);
	}

	gpioWrite(sckP, 1);
	gpioDelay(2);
	gpioWrite(sckP, 0);
	gpioDelay(2);

	if(send_ack){
		gpioSetMode(dtaP, 0);
		gpioDelay(2);
	}
	return value;
}

unsigned char SHT1x_Get_Measure_Value(void){
	unsigned char checksum, hiby, loby;
	unsigned char noerrsta = 1;
	unsigned char delay_count = 62;

	while(gpioRead(dtaP)){
		gpioDelay(5000);
		delay_count--;
		if(delay_count == 0) return 0;
	}

	hiby = SHT1x_Readbyte(TRUE);
	SHT1x_Crc_Check(hiby);
	loby = SHT1x_Readbyte(TRUE);
	SHT1x_Crc_Check(loby);

	checksum = SHT1x_Readbyte(FALSE);
	if(SHT1x_Mirrorbyte(checksum) == SHT1x_crc){
		tHibyte = hiby;
		tLobyte = loby;
		return TRUE;
	}
	else return FALSE;
}

float SHT1x_Calc(float value){
	float t_C;
	const float	D1 = -39.66;
	const float	D2 = 0.01;
	t_C = D1 + (D2 * value);
	return t_C;
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
	noerrsta = SHT1x_Measure_Start(0x03); //Temperature command
	if(noerrsta == 0) return;
	noerrsta = SHT1x_Get_Measure_Value();
	if(noerrsta == 0) return;
	unsigned short int tempint;
	tempint = tHibyte << 8;
	tempint += tLobyte;
	float fintemp = (float)tempint;
	fintemp = SHT1x_Calc(fintemp);
	printf("Temperature: %0.2f%cC\n",fintemp,0x00B0);

	gpioTerminate();
	return 0;
}
