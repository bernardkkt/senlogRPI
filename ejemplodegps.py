import gps
import threading

loc = ['','']
alive = True

def startDmn(inhSession):
	global loc
	global alive
	while alive:
		try:
			report = inhSession.next()
			if hasattr(report, 'lat') and hasattr(report, 'lon'):
				loc[0] = report.lat
				loc[1] = report.lon
		except:
			print "Interrupted. Exiting..."
			break

class GLoc:
	def __init__(self):
		global loc
		self.session = gps.gps("127.0.0.1", "2947")
		self.session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
		
	def getLoc(self):
		threading.Thread(target = startDmn, args = (self.session,))

def main():
	global alive
	global loc
	hazel = GLoc()
	hazel.getLoc()
	
	while True:
		try:
			raw_input("Press enter to get the coordinates.")
			print str(loc[0]) + ", " + str(loc[1])
			print
		except:
			print "Exiting..."
			alive = False
	return 0

if __name__ == '__main__':
	main()

