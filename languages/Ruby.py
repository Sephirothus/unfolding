from Helper import Helper
from dists.RouterDist import RouterDist

class Ruby(RouterDist):

	name = 'Ruby'
	serviceName = 'ruby-full'
	commandName = 'ruby'
	
	def installUbuntu(self):
		self.currentDist.aptGet(self.serviceName)

	def deleteUbuntu(self):
		self.currentDist.removeAptGet(self.serviceName)

	def check(self):
		return (Helper()).checkVersion(self.commandName)
