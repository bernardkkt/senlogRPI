import time, pigpio, os
from sht1x.Sht1x import Sht1x as SHT1x
import Adafruit_BMP.BMP085 as BMP180

tempdataPin = 11
tempclkPin = 7
ins2rd = [0x22, 0x00, 0x08, 0x2A]
samplingtime = 10

def checkFile():
	dia = time.strftime("%d-%m-%Y") + ".csv"
	csvf = open(dia, "a+")
	if os.stat(dia).st_size == 0:
	  csvf.write("Date-Time,Temperature,BMPTemperature,Humidity,Pressure,CO2\n")
	  csvf.flush()
	return csvf

def gCO2(mano, enu):
	try:
		mano.i2c_write_device(enu, ins2rd)
		time.sleep(0.02)
		cnt, taf = mano.i2c_read_device(enu, 4)
		if taf[3] == ((taf[0]+taf[1]+taf[2])%256):
			ccVal = (taf[1]*256) + taf[2]
		else:
			ccVal = "N/A"
	except:
		ccVal = "N/A"
	return ccVal

def gBaro(mano):
	try:
		bpa = mano.read_pressure()
		btp = mano.read_temperature()
	except:
		bpa = "N/A"
		btp = "N/A"
	return bpa, btp

def main():
	#Initialisation
	pi = pigpio.pi()
	co2 = pi.i2c_open(1, 0x68)
	sht71 = SHT1x(tempdataPin, tempclkPin, SHT1x.GPIO_BOARD)
	bsense = BMP180.BMP085()
	selfil = checkFile()
	
	#Initiate with start time
	nt = int(time.time())
	print "\n" + "Current start time: " + time.ctime(nt) + "\n"
	
	#Sampling and logging	
	try:
		while True:
			ct = int(time.time())
			if nt == ct:
				nt = ct + samplingtime
				timestamp = time.ctime(ct)
				spt = timestamp.split()
				
				baroval, tmpval = gBaro(bsense)
				tempval = sht71.read_temperature_C()
				humdval = sht71.read_humidity()				
				co2val = gCO2(pi, co2)
				
				twrite = "Temperature in C: " + str(tempval) + "\n" + "Temperature (by BMP) in C: " + str(tmpval) + "\n" + "Humidity in %: " + str(humdval) + "\n" + "Pressure in Pa: " + str(baroval) + "\n" + "CO2 concentration in ppm: " + str(co2val)
				
				pwrite = time.strftime("%d-%m-%Y") + " " + spt[3] + "," + str(tempval) + "," + str(tmpval) + "," + str(humdval) + "," + str(baroval) + "," + str(co2val) + "\n"
				
				selfil.write(pwrite)
				selfil.flush()				
				print twrite
				print "Data logged at: " + str(spt[3]) + "\n"
	except KeyboardInterrupt:
		print "Closing..."
		pi.stop()
			
	return 0

if __name__ == '__main__':
	main()
