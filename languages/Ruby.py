from Helper import Helper

class Ruby:

	name = 'Ruby'
	serviceName = 'ruby-full'
	commandName = 'ruby'
	
	def installUbuntu(self):
		self.curDist.aptGet(self.serviceName)

	def deleteUbuntu(self):
		self.curDist.removeAptGet(self.serviceName)

	def check(self):
		return (Helper()).checkVersion(self.commandName)
