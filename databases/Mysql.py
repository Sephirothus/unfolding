from Helper import Helper

class Mysql:

	name = "MySQL"
	serverName = 'mysql'
	defaultRootPass = '1'
	packages = {
		'mysql': 'mysql-server', 
		'mariadb': {
			'service_name': 'mariadb-server',
			'deb_conf': 'mariadb-server mariadb-server/oneway_migration	boolean	true'
		},
		'percona': {
			'service_name': 'percona-server-server',
			'download_url': 'https://repo.percona.com/apt/percona-release_0.1-3.{$lsb_release}_all.deb',
			'deb_conf': 'percona-server-server percona-server-server/postrm_remove_databases boolean true'
		}
	}
	
	def installUbuntu(self):
		package = self.getPackage()
		packageName = self.getPackageName()
		self.curDist.debConfSetSelections([
			packageName + ' ' + packageName + '/root_password password ' + self.defaultRootPass,
			packageName + ' ' + packageName + '/root_password_again password ' + self.defaultRootPass
		])
		self.curDist.execMethod(package['name'] + 'Setup', self, package)
		self.curDist.aptGet(packageName)

	def deleteUbuntu(self):
		self.curDist.removeAptGet(self.getPackageName())
		
	def configure(self):
		helper = Helper()
		user = 'root'
		password = self.defaultRootPass
		if 'user' in self.attrs and 'password' in self.attrs:
			print "-- Creating user with all privilages"
			helper.mysqlCommand('GRANT ALL PRIVILEGES ON *.* TO \'' + self.attrs['user'] + '\' IDENTIFIED BY \'' + self.attrs['password'] + '\'', user, password)
			user = self.attrs['user']
			password = self.attrs['password']
		if 'db' in self.attrs:
			print "-- Creating database"
			helper.mysqlCommand('CREATE DATABASE IF NOT EXISTS ' + self.attrs['db'], user, password)

	def check(self):
		return (Helper()).checkVersion(self.serverName)

	def getPackage(self):
		key = self.attrs['build'] if 'build' in self.attrs and self.attrs['build'] in self.packages else 'mysql'
		return (Helper()).mergeDicts(self.packages[key], {'name': key}) if type(self.packages[key]) is dict else self.packages[key]

	def getPackageName(self):
		package = self.getPackage()
		return package['service_name'] if type(package) is dict else package

	# builds setups
	def perconaSetup(self, data):
		helper = Helper()
		helper.wgetDpkg(data['download_url'].replace('{$lsb_release}', helper.getLsbRelease()))
		self.curDist.aptGetUpdate()
		helper.debConfSetSelections(data['deb_conf'])

	def mariadbSetup(self, data):
		(Helper()).debConfSetSelections(data['deb_conf'])
