import time, pigpio, os, threading, sys
from gps import *
from sht1x.Sht1x import Sht1x as SHT1x
import Adafruit_BMP.BMP085 as BMP180

tempdataPin = 11
tempclkPin = 7
ins2rd = [0x22, 0x00, 0x08, 0x2A]
samplingtime = 10
sensorData = [None]*7
alive = None

class Sensors:
	def __init__(self):
		try:
			mark = 1

			self.pi = pigpio.pi()
			self.k30 = self.pi.i2c_open(1, 0x68)
			mark = mark + 1

			self.sht71 = SHT1x(tempdataPin, tempclkPin, SHT1x.GPIO_BOARD)
			mark = mark + 1

			self.bsense = BMP180.BMP085()
		except:
			print "Unsuccessful initialisation. Error code: " + str(mark)
			if mark is not 1:
				self.pi.stop()
			sys.exit(0)
	
	def startGPS(self):
		try:
			self.gsession = gps(mode=WATCH_ENABLE)
			sFlag = True
		except:
			print "Cannot initialise GPS backend. GPS data might be unavailable."
		
		if sFlag is True:
			th = threading.Thread(target = startDmn, args = (self.gsession,))
			th.start()			
		else:
			global sensorData
			sensorData[5] = "N/A"
			sensorData[6] = "N/A"
		
	def startThreads(self):
		try:
			th1 = threading.Thread(target=gCO2, args=(self.pi, self.k30,))
			th2 = threading.Thread(target=gBaro, args=(self.bsense,))
			th3 = threading.Thread(target=gSHT, args=(self.sht71,))

			th2.start()
			th2.join()
			th1.start()
			th3.start()

			th1.join()
			th3.join()
		except:
			print "Unsuccessful calling. Exiting..."
			self.pi.stop()
			sys.exit(0)

	def cleanExit(self):
			self.pi.stop()
			sys.exit(0)

def startDmn(inhSession):
	global sensorData
	global alive
	sensorData[5] = "N/A"
	sensorData[6] = "N/A"
	while alive:
		try:
			inhSession.next()
			sensorData[5] = inhSession.fix.latitude
			sensorData[6] = inhSession.fix.longitude
		except:
			sensorData[5] = "N/A"
			sensorData[6] = "N/A"
		time.sleep(0.000001)

def gCO2(mano, enu):
	try:
		mano.i2c_write_device(enu, ins2rd)
		time.sleep(0.02)
		cnt, taf = mano.i2c_read_device(enu, 4)

		if taf[3] == ((taf[0]+taf[1]+taf[2])%256):
			ccVal = (taf[1]*256) + taf[2]
		else:
			ccVal = "-1"

		if ccVal > 10000:
			ccVal = "-2"
	except:
		ccVal = "-3"

	global sensorData
	sensorData[0] = ccVal

def gSHT(mano):
	try:
		tempval = mano.read_temperature_C()
		humdval = mano.read_humidity()
	except:
		tempval = "N/A"
		humdval = "N/A"

	global sensorData
	sensorData[1] = tempval
	sensorData[2] = humdval

def gBaro(mano):
	try:
		bpa = mano.read_pressure()
		btp = mano.read_temperature()
	except:
		bpa = "N/A"
		btp = "N/A"

	global sensorData
	sensorData[3] = bpa
	sensorData[4] = btp

def checkFile():
	dia = time.strftime("%d-%m-%Y") + ".csv"
	csvf = open(dia, "a+")
	if os.stat(dia).st_size == 0:
	  csvf.write("Date and Time,Temperature,BMPTemperature,Humidity,Pressure,CO2,Corrected CO2,Latitude,Longitude\n")
	  csvf.flush()
	return csvf

def correct(inpppm, inpbaro):
	if int(inpppm) >= 0:
		inpbaro = inpbaro / 1000.0
		factor = (4.026 * 0.001 * inpbaro) + (5.780 * 0.00001 * inpbaro * inpbaro)
		trueVal = inpppm / factor
		trueVal = int(round(trueVal))
	else:
		trueVal = "N/A"
	return trueVal

def main():
	#Initialisation
	global sensorData
	allsensors = Sensors()
	allsensors.startGPS()
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
				allsensors.startThreads()
				pcomp = correct(sensorData[0], sensorData[3])

				twrite = "Temperature in C: " + str(sensorData[1]) + "\n" + "Temperature (by BMP) in C: " + str(sensorData[4]) + "\n" + "Humidity in %: " + str(sensorData[2]) + "\n" + "Pressure in Pa: " + str(sensorData[3]) + "\n" + "CO2 concentration in ppm: " + str(sensorData[0]) + "\n" + "Corrected CO2 ppm: " + str(pcomp) + "\n" + "Latitude: " + str(sensorData[5]) + "\n" + "Longitude: " + str(sensorData[6])

				pwrite = time.strftime("%d-%m-%Y") + " " + spt[3] + "," + str(sensorData[1]) + "," + str(sensorData[4]) + "," + str(sensorData[2]) + "," + str(sensorData[3]) + "," + str(sensorData[0]) + "," + str(pcomp) + "," + str(sensorData[5]) + "," + str(sensorData[6]) + "\n"

				selfil.write(pwrite)
				selfil.flush()
				print twrite
				print "Data logged at: " + str(spt[3]) + "\n"
			time.sleep(0.000001)
	except KeyboardInterrupt:
		print "Closing..."
		allsensors.cleanExit()
	return 0

if __name__ == '__main__':
	main()
