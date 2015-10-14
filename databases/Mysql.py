from dists.Ubuntu import Ubuntu
from Helper import Helper

class Mysql:

	name = "MySQL"
	
	def installUbuntu(self):
		myDist = Ubuntu()
		print myDist.aptGet('mysql-server')
		
	def configure(self):
		helper = Helper()
		user = 'root'
		password = ''
		if 'user' in self.attrs and 'password' in self.attrs:
			print "-- Creating user with all privilages"
			user = self.attrs['user']
			password = self.attrs['password']
			helper.execute(helper.mysqlCommand('CREATE USER \'' + user + '\' IDENTIFIED BY \'' + password + '\''))
			helper.execute(helper.mysqlCommand('GRANT ALL PRIVILEGES ON * . * TO \'' + user + '\''))
		if 'db' in self.attrs:
			print "-- Creating database"
			helper.execute(helper.mysqlCommand('create database ' + self.attrs['db'], user, password))

	def check(self):
		return "mysql  Ver" in (Helper()).execute("mysql --version")