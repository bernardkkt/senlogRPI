import requests
import time
import threading

def ping2url(url):
	stime = time.time()
	conn = requests.head(url)
	ttime = time.time() - stime
	if conn.status_code is not 200:
		print "Unexpected behavior detected: " + url + " (" + str(conn.status_code) + ")"
	else:
		print "Success: " + str(ttime) + " (" + url + ")"

def main():
	urls = ['http://g.co', 'http://www.baidu.com', 'http://www.rai.it', 'http://www.rtve.es', 'http://www.bbc.co.uk', 'http://p3.no']
	
	print str(time.time())
	for url in urls:
		handsle = threading.Thread(target = ping2url, args = (url,))
		handsle.start()
	print "Threads have been started."
	
	for proc in threading.enumerate():
		if proc.getName() is "MainThread":
			pass
		else:
			proc.join()
	
	print "El fin: " + str(time.time())
	return 0

if __name__ == '__main__':
	main()

