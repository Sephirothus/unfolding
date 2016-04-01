from Helper import Helper

class Mongo:

	name = "MongoDB"

	serviceName = 'mongodb-org'
	serverName = 'mongodb'
	key = '--keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927',
	rep = 'deb http://repo.mongodb.org/apt/ubuntu {$lsb_release}/mongodb-org/3.2 multiverse'
	dbFolder = '/var/log/mongodb'
	logsFolder = '/var/lib/mongodb'
	
	def installUbuntu(self):
		self.curDist.aptGet(self.serviceName, self.rep, self.key)

	def deleteUbuntu(self):
		self.curDist.servStop(self.serverName)
		self.curDist.removeAptGet(self.serviceName + '*', self.rep)
		(Helper()).rm(self.dbFolder + ' ' + self.logsFolder)
