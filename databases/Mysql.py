from dists.Ubuntu import Ubuntu
from Helper import Helper

class Mysql:

	name = "MySQL"
	
	def installUbuntu(self):
		myDist = Ubuntu()
		myDist.execute('echo "mysql-server mysql-server/root_password password 1" | sudo debconf-set-selections', True)
		myDist.execute('echo "mysql-server mysql-server/root_password_again password 1" | sudo debconf-set-selections', True)
		print myDist.aptGet('mysql-server')

	def removeUbuntu(self):
		return (Ubuntu()).removeAptGet('mysql-server')
		
	def configure(self):
		helper = Helper()
		user = 'root'
		password = '1'
		if 'user' in self.attrs and 'password' in self.attrs:
			print "-- Creating user with all privilages"
			helper.execute(helper.mysqlCommand('CREATE USER \'' + self.attrs['user'] + '\' IDENTIFIED BY \'' + self.attrs['password'] + '\'', user, password))
			helper.execute(helper.mysqlCommand('GRANT ALL PRIVILEGES ON * . * TO \'' + self.attrs['user'] + '\'', user, password))
			user = self.attrs['user']
			password = self.attrs['password']
		if 'db' in self.attrs:
			print "-- Creating database"
			helper.execute(helper.mysqlCommand('create database ' + self.attrs['db'], user, password))

	def check(self):
		return (Helper()).checkVersion('mysql')
