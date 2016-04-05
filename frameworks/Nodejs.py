from Helper import Helper
from dists.RouterDist import RouterDist

class Nodejs(RouterDist):

	name = 'Node.js'
	serviceName = 'nodejs'

	def installUbuntu(self):
		self.currentDist.aptGet(self.serviceName)

	def deleteUbuntu(self):
		self.currentDist.removeAptGet(self.serviceName)

	def check(self):
		return (Helper()).checkVersion(self.serviceName)
