from Helper import Helper
from dists.RouterDist import RouterDist

class Ruby(RouterDist):

	name = 'Ruby'
	serviceName = 'ruby-full'
	commandName = 'ruby'
	
	def installUbuntu(self):
		self.dist.aptGet(self.serviceName)

	def deleteUbuntu(self):
		self.dist.removeAptGet(self.serviceName)

	def check(self):
		return (Helper()).checkVersion(self.commandName)
