from dists.Ubuntu import Ubuntu
from Helper import Helper

class Mysql:

	name = "MySQL"
	
	def installUbuntu(self):
		myDist = Ubuntu()
		user = 'root'
		password = ''
		print myDist.aptGet('mysql-server')
		
	def configure(self):
		helper = Helper()
		if 'user' in self.attrs and 'password' in self.attrs:
			print "-- Creating user with all privilages"
			user = self.attrs['user']
			password = self.attrs['password']
			helper.execute('echo "CREATE USER \'' + user + '\' IDENTIFIED BY \'' + password + '\';"' + helper.mysqlCommand())
			helper.execute('echo "GRANT ALL PRIVILEGES ON * . * TO \'' + user + '\';"' + helper.mysqlCommand())
		if 'db' in self.attrs:
			print "-- Creating database"
			helper.execute('echo "create database ' + self.attrs['db'] + '"' + helper.mysqlCommand(user, password))

	def check(self):
		return "mysql  Ver" in (Helper()).execute("mysql --version")