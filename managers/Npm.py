from Helper import Helper

class Npm:

	name = 'npm'

	def installUbuntu(self):
		self.curDist.aptGet(self.name)

	def check(self):
		return (Helper()).checkVersion(self.name)

	def deleteUbuntu(self):
		self.curDist.removeAptGet(self.name)
