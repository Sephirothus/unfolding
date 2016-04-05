from Helper import Helper
from dists.RouterDist import RouterDist

class Sphinx(RouterDist):

	name = "Sphinx"
	serviceName = 'sphinxsearch'
	serverName = 'searchd'
	
	def installUbuntu(self):
		self.currentDist.aptGet(self.serviceName)

	def deleteUbuntu(self):
		self.currentDist.removeAptGet(self.serviceName)

	def check(self):
		return (Helper()).checkVersion(self.serverName)
		