class Apache:

	def install(self, myDist):
		myDist.createBlock("Installing Apache")
		if self.check(myDist):
			print "Apache2 already installed"
		else:
			myDist.aptGet('apache2')

	def check(self, myDist):
		exist = myDist.execute("sudo service apache2 status")
		return "unrecognized service" not in exist