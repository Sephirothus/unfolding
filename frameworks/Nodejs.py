from Helper import Helper

class Nodejs:

	name = 'Node.js'
	serviceName = 'nodejs'

	def installUbuntu(self):
		self.curDist.aptGet(self.serviceName)

	def deleteUbuntu(self):
		self.curDist.removeAptGet(self.serviceName)

	def check(self):
		return (Helper()).checkVersion(self.serviceName)
