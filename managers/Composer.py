from dists.Ubuntu import Ubuntu

class Composer:

	dependencies = ['languages.Php', 'extensions.Curl']
	name = 'Composer'

	def installUbuntu(self):
		myDist = Ubuntu()
		myDist.execute('sudo curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer')
		myDist.execute('sudo composer global require "fxp/composer-asset-plugin:~1.0.3"')
		
	def checkUbuntu(self):
		return "version" in (Ubuntu()).execute("composer --version")
