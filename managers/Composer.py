from Helper import Helper
from dists.RouterDist import RouterDist

class Composer(RouterDist):

	dependencies = ['languages.Php', 'extensions.Curl']
	name = 'Composer'
	commandName = 'composer'

	def install(self):
		myDist.execute('curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer', True)
		myDist.execute('sudo composer global require "fxp/composer-asset-plugin:~1.0.3"', True)
		
	def check(self):
		return (Helper()).checkVersion(self.commandName)
