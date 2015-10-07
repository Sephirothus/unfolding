class Php:
	
	def install(self, myDist):
		rep = False
		command = ''
		if hasattr(self, 'attrs'):
			if 'version' in self.attrs:
				version = self.attrs['version']
				if version == '5.4':
					rep = 'ppa:ondrej/php5-oldstable'
				elif version == '5.5':
					rep = 'ppa:ondrej/php5'
				elif version == '5.6':
					rep = 'ppa:ondrej/php5-5.6'

			if 'type' in self.attrs:
				command = self.attrs['type']

		print "==================\nInstalling PHP 5\n"
		myDist.aptGet(command, rep)
		print "=================="
