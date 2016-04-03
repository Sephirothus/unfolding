from Helper import Helper
from dists.RouterDist import RouterDist

class Mysql(RouterDist):

	name = "MySQL"

	serverName = 'mysql'
	defaultRootPass = '1'
	defaultPackage = 'mysql'
	packages = {
		'mysql': {
			'service_name': 'mysql-server'
		},
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
		self.dist.debConfSetSelections([
			package['service_name'] + ' ' + package['service_name'] + '/root_password password ' + self.defaultRootPass,
			package['service_name'] + ' ' + package['service_name'] + '/root_password_again password ' + self.defaultRootPass
		])
		self.dist.execPackageMethod('install', self, package)
		self.dist.aptGet(package['service_name'])

	def deleteUbuntu(self):
		package = self.getPackage()
		self.dist.execPackageMethod('delete', self, package)
		self.dist.removeAptGet(package['service_name'])
		
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

	# packages installs
	def perconaInstall(self, data):
		helper = Helper()
		helper.wgetDpkg(helper.getLsbRelease(data['download_url']))
		self.dist.aptGetUpdate()

	def mariadbInstall(self, data):
		(Helper()).debConfSetSelections(data['deb_conf'])

	def perconaDelete(self, data):
		# delete not works
		(Helper()).debConfSetSelections(data['deb_conf'])
