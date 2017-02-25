from gps import *
import threading

loc = [None]*2
alive = None

def startDmn(inhSession):
	global alive
	global loc
	print str(alive)
	try:
		while alive:
			inhSession.next()
			loc[0] = inhSession.fix.latitude
			loc[1] = inhSession.fix.longitude
	except:
		print "Unexpected error."

class GLoc:
	def __init__(self):
		self.gsession = gps(mode=WATCH_ENABLE)
	def getLoc(self):
		th = threading.Thread(target = startDmn, args = (self.gsession,))
		th.start()
		print "done p1"

def main():
	global alive
	global loc
	alive = True
	hazel = GLoc()
	hazel.getLoc()
	
	try:
		while True:
			raw_input("Press enter to get the coordinates.")
			print str(loc[0]) + ", " + str(loc[1])
			print
	except:
		print "Exiting..."
		alive = False
	
	return 0

if __name__ == '__main__':
	main()
