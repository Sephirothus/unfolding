from dists.Ubuntu import Ubuntu
from databases.Mysql import Mysql
from Helper import Helper

class Php:

	name = "PHP"
	sortOrder = ["databases"]
	
	def installUbuntu(self):
		myDist = Ubuntu()
		command = self.getCommandName()
		print myDist.aptGet(command['command'], command['rep'], command['version'])
		print myDist.aptGet(command['command'] + ('-fpm' if command['isFpm'] else ''))

	def configureUbuntu(self):
		modules = self.getModules()
		if (modules):
			print "-- installing " + modules
			print (Ubuntu()).aptGet(modules)

	def check(self):
		return (Helper()).checkVersion('php')

	def deleteUbuntu(self):
		command = self.getCommandName()
		return (Ubuntu()).removeAptGet(command['command'] + '*', command['rep'])

	def getModules(self):
		modules = False
		command = self.getCommandName()['command']
		if 'modules' in self.attrs:
			modules = self.attrs['modules']
			if modules == 'default':
				modules = ['mcrypt', 'curl', 'gd', 'intl', 'json']

				# checking if dbs installed, then install extensions for them
				if (Mysql()).check():
					modules.append('mysql')

			modules = ' '.join([command + '-' + mod for mod in modules])
		return modules

	def getCommandName(self):
		rep = False
		command = 'php5'
		version = False
		isFpm = False
		if hasattr(self, 'attrs'):
			if 'version' in self.attrs:
				version = self.attrs['version']
				if version == '5.4':
					rep = 'ppa:ondrej/php5-oldstable'
				elif version == '5.5':
					rep = 'ppa:ondrej/php5'
				elif version == '5.6':
					rep = 'ppa:ondrej/php5-5.6'
				elif version == '7.0':
					rep = 'ppa:ondrej/php'
					command = 'php7.0'
					version = False
			if 'is_fpm' in self.attrs:
				isFpm = self.attrs['is_fpm']

		return {'command': command, 'rep': rep, 'isFpm': isFpm, 'version': version}