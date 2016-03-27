from Helper import Helper

class Sphinx:

	name = "Sphinx"
	serviceName = 'sphinxsearch'
	serverName = 'searchd'
	
	def installUbuntu(self):
		self.curDist.aptGet(self.serviceName)

	def deleteUbuntu(self):
		self.curDist.removeAptGet(self.serviceName)

	def check(self):
		return (Helper()).checkVersion(self.serverName)
		