from Helper import Helper
from dists.RouterDist import RouterDist

class Npm(RouterDist):

	name = 'npm'

	def installUbuntu(self):
		self.dist.aptGet(self.name)

	def check(self):
		return (Helper()).checkVersion(self.name)

	def deleteUbuntu(self):
		self.dist.removeAptGet(self.name)
