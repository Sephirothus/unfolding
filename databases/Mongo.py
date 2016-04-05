from dists.RouterDist import RouterDist

class Mongo(RouterDist):

	name = "MongoDB"

	serviceName = 'mongodb-org'
	repository = 'deb http://repo.mongodb.org/apt/ubuntu {$lsb_release}/mongodb-org/3.2 multiverse'
	key = '--keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927'
	checkName = 'mongo'
	serverName = 'mongodb'
	dbFolder = '/var/log/mongodb'
	logsFolder = '/var/lib/mongodb'

	def beforeDelete(self):
		self.currentDist.servStop(self.serverName)

	def afterDelete(self):
		self.rm(self.dbFolder + ' ' + self.logsFolder)
