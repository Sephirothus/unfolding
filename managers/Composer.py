from dists.Ubuntu import Ubuntu
from Helper import Helper

class Composer:

	dependencies = ['languages.Php', 'extensions.Curl']
	sortOrder = ['languages.Php', 'extensions.Curl']
	name = 'Composer'

	def installUbuntu(self):
		myDist = Ubuntu()
		myDist.execute('curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer', True)
		myDist.execute('sudo composer global require "fxp/composer-asset-plugin:~1.0.3"', True)
		
	def check(self):
		return (Helper()).checkVersion('composer')
