from dists.RouterDist import RouterDist
from databases.Mysql import Mysql
from servers.Apache import Apache
from servers.Nginx import Nginx
from Helper import Helper

class Php(RouterDist):

	name = "PHP"
	sortOrder = ["databases"]

	serverName = 'php'
	defaultModules = ['mcrypt', 'curl', 'gd', 'intl', 'json']
	defaultPackage = '5.6'
	packages = {
		'5.4': {
			'methodPrefix': 'php',
			'command': 'php5',
			'rep': 'ppa:ondrej/php5-oldstable'
		},
		'5.5': {
			'methodPrefix': 'php',
			'command': 'php5',
			'rep': 'ppa:ondrej/php5'
		},
		'5.6': {
			'methodPrefix': 'php',
			'command': 'php5',
			'rep': 'ppa:ondrej/php5-5.6'
		},
		'7.0': {
			'methodPrefix': 'php',
			'command': 'php7.0',
			'rep': 'ppa:ondrej/php',
		},
		'hhvm': {
			'command': 'hhvm',
			'key': '--recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0x5a16e7281be7a449',
			'rep': 'deb http://dl.hhvm.com/ubuntu {$lsb_release} main',
		}
	}
	
	def installUbuntu(self):
		self.currentDist.execPackageMethod('install', self, self.getPackage())

	def configureUbuntu(self):
		self.currentDist.execPackageMethod('configure', self, self.getPackage())

	def check(self):
		return (Helper()).checkVersion(self.serverName)

	def deleteUbuntu(self):
		package = self.getPackage()
		self.currentDist.execPackageMethod('delete', self, package)
		self.currentDist.removeAptGet(package['command'] + '*', package['rep'])

	def getPackage(self):
		return (Helper()).getPackageInfo('version', self.attrs, self.packages, self.defaultPackage)

	# packages installs
	def hhvmInstall(self, data):
		self.currentDist.aptGet(data['command'], (Helper()).getLsbRelease(data['rep']), data['key'])

	def phpInstall(self, data):
		self.currentDist.aptGet(data['command'], data['rep'], False, data['index'])
		if 'is_fpm' in self.attrs: self.currentDist.aptGet(data['command'] + '-fpm')

	# packages configure
	def hhvmConfigure(self, data):
		self.currentDist.execute('/usr/share/hhvm/install_fastcgi.sh')

	def phpConfigure(self, data):
		modules = self.getModules()
		if (modules):
			print "-- installing " + modules
			print self.currentDist.aptGet(modules)

	def getModules(self):
		modules = False
		if 'modules' in self.attrs:
			command = self.getPackage()['command']
			modules = self.attrs['modules']
			if modules == 'default':
				modules = self.defaultModules

				# checking if dbs installed, then install extensions for them
				if (Mysql()).check():
					modules.append('mysql')

			modules = ' '.join([command + '-' + mod for mod in modules])
		return modules

	# packages delete
	def hhvmDelete(self, data):
		self.currentDist.execute('/usr/share/hhvm/uninstall_fastcgi.sh')
		(Apache()).restart()
		(Nginx()).restart()