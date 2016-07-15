from dists.RouterDist import RouterDist

class Mysql(RouterDist):

	name = "MySQL"

	checkName = 'mysql'
	defaultRootPass = '1'
	defaultPackage = 'mysql'
	packageAttr = 'build'
	
	def beforeInstallDebian(self, package):
		self.debConfSetSelections([
			package['serviceName'] + ' ' + package['serviceName'] + '/root_password password ' + self.defaultRootPass,
			package['serviceName'] + ' ' + package['serviceName'] + '/root_password_again password ' + self.defaultRootPass
		])
		self.execPackageMethod('install', self, package)

	def beforeDelete(self, package):
		self.execPackageMethod('delete', self, package)
		
	def configure(self):
		user = 'root'
		password = self.defaultRootPass
		if 'user' in self.attrs and 'password' in self.attrs:
			print "-- Creating user with all privilages"
			self.mysqlCommand('GRANT ALL PRIVILEGES ON *.* TO \'' + self.attrs['user'] + '\' IDENTIFIED BY \'' + self.attrs['password'] + '\'', user, password)
			user = self.attrs['user']
			password = self.attrs['password']
		if 'db' in self.attrs:
			print "-- Creating database"
			self.mysqlCommand('CREATE DATABASE IF NOT EXISTS ' + self.attrs['db'], user, password)

	# packages installs
	def perconaInstallDebian(self, data):
		self.wgetAddpkg(self.currentDist.getRelease(data['download_url']))

	def mariadbInstallDebian(self, data):
		self.debConfSetSelections(data['deb_conf'])

	def perconaDeleteDebian(self, data):
		# delete not works
		self.debConfSetSelections(data['deb_conf'])
