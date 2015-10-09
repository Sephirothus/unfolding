from Helper import Helper

class Ubuntu:

	conf = {}
	helper = False

	def __init__(self, conf={}):
		self.conf = conf
		self.helper = Helper()

	def aptGet(self, name, rep=False):
		if rep:
			self.execute('sudo add-apt-repository ' + rep)
			self.execute('sudo apt-get update')

		print self.execute('sudo apt-get install -y ' + name)

	def install(self):
		return False

	def execute(self, command):
		return self.helper.execute(command)

	def createBlock(self, string):
		return self.helper.createBlock(string)