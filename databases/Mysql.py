from Helper import Helper

class Mysql:

	name = "MySQL"

	serverName = 'mysql'
	defaultRootPass = '1'
	defaultPackage = 'mysql'
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
		self.curDist.execPackageMethod('install', self, package)
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
		return (Helper()).getPackageInfo('build', self.attrs, self.packages, self.defaultPackage)

	def getPackageName(self):
		package = self.getPackage()
		return package['service_name'] if type(package) is dict else package

	# packages installs
	def perconaInstall(self, data):
		helper = Helper()
		helper.wgetDpkg(helper.getLsbRelease(data['download_url']))
		self.curDist.aptGetUpdate()
		helper.debConfSetSelections(data['deb_conf'])

	def mariadbInstall(self, data):
		(Helper()).debConfSetSelections(data['deb_conf'])
