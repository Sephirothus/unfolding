from Helper import Helper

class Ubuntu(Helper):

	def aptGet(self, name, rep=False):
		if rep:
			self.execute('sudo add-apt-repository ' + rep)
			self.execute('sudo apt-get update')

		return self.execute('sudo apt-get install --yes --force-yes ' + name)

	def composerProject(self, params):
		return self.execute('sudo composer create-project --prefer-dist '+params)

	def wgetUntar(self, filePath):
		fileName = filePath.rsplit('/', 1)[1]
		self.execute('wget -P /tmp ' + filePath)
		self.execute('tar xvzf /tmp/' + fileName + ' -C /tmp')
		self.execute('rm /tmp/' + fileName)

	def install(self):
		return False

	def servStatus(self, service):
		return self.execute('sudo service ' + service + ' status')
