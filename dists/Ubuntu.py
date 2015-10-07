from Helper import Helper

class Ubuntu:
	
	conf = {}
	helper = False

	def __init__(self, conf={}):
		self.conf = conf
		self.helper = Helper()

	def aptGet(self, name, rep=False):
		if rep:
			self.helper.execute('sudo add-apt-repository ' + rep)
			self.helper.execute('sudo apt-get update')

		print self.helper.execute('sudo apt-get install -y ' + name)

	def install(self):
		return False