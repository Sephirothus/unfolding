from Helper import Helper
from dists.RouterDist import RouterDist

class Sphinx(RouterDist):

	name = "Sphinx"
	serviceName = 'sphinxsearch'
	serverName = 'searchd'
	
	def installUbuntu(self):
		self.dist.aptGet(self.serviceName)

	def deleteUbuntu(self):
		self.dist.removeAptGet(self.serviceName)

	def check(self):
		return (Helper()).checkVersion(self.serverName)
		