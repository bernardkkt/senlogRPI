count = 0

class Sensors:
	def __init__(self):
		global count
		count += 1
		self.session = count
		
	def K30(self):
		frase = "This is K30: " + str(self.session)
		return frase
		
	def BMP(self):
		frase = "This is BMP: " + str(self.session)
		return frase
		
	def SHTT(self):
		frase = "This is SHTT: " + str(self.session)
		return frase
		
	def SHTH(self):
		frase = "This is SHTH: " + str(self.session)
		return frase
		
	def LOC(self):
		frase = "This is LOC: " + str(self.session)
		return frase

def main():
	bene = Sensors()
	print bene.K30()
	print bene.BMP()
	print bene.SHTT()
	print bene.SHTH()
	print bene.LOC()
	print '='*22
	male = Sensors()
	print male.K30()
	print male.BMP()
	print male.SHTT()
	print male.SHTH()
	print male.LOC()
	print '='*22
	print bene.K30()
	print bene.BMP()
	print bene.SHTT()
	print bene.SHTH()
	print bene.LOC()
	print '='*22
	return 0

if __name__ == '__main__':
	main()

