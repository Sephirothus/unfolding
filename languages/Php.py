from dists.Ubuntu import Ubuntu
from databases.Mysql import Mysql
from servers.Apache import Apache
from servers.Nginx import Nginx
from Helper import Helper

class Php:

	name = "PHP"
	sortOrder = ["databases"]
	
	def installUbuntu(self):
		myDist = Ubuntu()
		command = self.getCommandName()
		myDist.aptGet(command['command'], command['rep'], command['key'], command['version'])
		if command['isFpm']: myDist.aptGet(command['command'] + '-fpm')

	def configureUbuntu(self):
		myDist = Ubuntu()
		command = self.getCommandName()['command']
		if (command == 'hhvm'):
			myDist.execute('/usr/share/hhvm/install_fastcgi.sh')
		else:
			modules = self.getModules()
			if (modules):
				print "-- installing " + modules
				print myDist.aptGet(modules)

	def check(self):
		return (Helper()).checkVersion('php')

	def deleteUbuntu(self):
		myDist = Ubuntu()
		command = self.getCommandName()
		if command['command'] == 'hhvm': 
			myDist.execute('/usr/share/hhvm/uninstall_fastcgi.sh')
			(Apache()).restart()
			(Nginx()).restart()
		myDist.removeAptGet(command['command'] + '*', command['rep'])

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
		key = False
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
				elif version == 'hhvm':
					key = '--recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0x5a16e7281be7a449'
					rep = 'deb http://dl.hhvm.com/ubuntu ' + (Helper()).execute('lsb_release -sc').strip() + ' main'
					command = 'hhvm'
					version = False
			if 'is_fpm' in self.attrs and ('version' not in self.attrs or self.attrs['version'] != 'hhvm'):
				isFpm = self.attrs['is_fpm']

		return {'command': command, 'rep': rep, 'isFpm': isFpm, 'version': version, 'key': key}
