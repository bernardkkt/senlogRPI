#rpi serial connections
#Python app to run a K-30 Sensor
import serial
import time

ser = serial.Serial("/dev/ttyUSB0",baudrate =9600,timeout = 2)
print "  AN-137: Raspberry Pi3 to K-30 Via UART\n"
ser.flushInput()
time.sleep(1)

while True:
	
    
    ser.flushInput()
    ser.write("\xFE\x44\x00\x08\x02\x9F\x25")
    time.sleep(.5)
    resp = ser.read(7)
    high = ord(resp[3])
    low = ord(resp[4])
    co2 = (high*256) + low
    print "CO2 = " +str(co2)
    time.sleep(.5)
