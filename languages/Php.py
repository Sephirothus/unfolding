from dists.Ubuntu import Ubuntu
from databases.Mysql import Mysql
from Helper import Helper

class Php:

	name = "PHP 5"
	
	def installUbuntu(self):
		myDist = Ubuntu()
		rep = False
		command = 'php5'
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

		print myDist.aptGet(command, rep)

	def configureUbuntu(self):
		myDist = Ubuntu()
		if 'extensions' in self.attrs:
			exts = self.attrs['extensions']
			if exts == 'all':
				exts = 'php5-mcrypt php5-curl php5-gd php5-dev'

				# checking if dbs installed, then istall extensions for them
				if (Mysql()).check():
					exts += ' php5-mysql'

			print myDist.aptGet(exts)

	def check(self):
		return (Helper()).checkVersion('php')
