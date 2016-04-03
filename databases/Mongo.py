from dists.RouterDist import RouterDist

class Mongo(RouterDist):

	name = "MongoDB"

	serviceName = 'mongodb-org'
	serverName = 'mongodb'
	checkName = 'mongo'
	key = '--keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927'
	rep = 'deb http://repo.mongodb.org/apt/ubuntu {$lsb_release}/mongodb-org/3.2 multiverse'
	dbFolder = '/var/log/mongodb'
	logsFolder = '/var/lib/mongodb'
	
	def installUbuntu(self):
		self.dist.aptGet(self.serviceName, self.getLsbRelease(self.rep), self.key)

	def deleteUbuntu(self):
		self.dist.servStop(self.serverName)
		self.dist.removeAptGet(self.serviceName + '*', self.rep)
		self.rm(self.dbFolder + ' ' + self.logsFolder)
