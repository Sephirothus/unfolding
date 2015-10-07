class Apache:

	def install(self, myDist):
        print "==================\nInstalling Apache 2.4\n"
        myDist.aptGet('apache2')
        print "=================="