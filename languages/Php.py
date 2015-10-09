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

			command = self.attrs['type'] if 'type' in self.attrs else 'php5'

		myDist.createBlock("Installing PHP 5")
		myDist.aptGet(command, rep)
