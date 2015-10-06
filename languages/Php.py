class Php:
	
	def install(self, myDist):
		rep = False
		command = ''
		if hasattr(self, 'attrs'):
			if 'version' in self.attrs:
				#if self.attrs['version']
				rep = False
			elif 'type' in self.attrs:
				command = val

		print "==================\nInstalling PHP 5\n"
		myDist.aptGet(command, rep)
		print "=================="
