class Ubuntu:
	conf = {}

	def __init__(self, conf={}):
		self.conf = conf

	def aptGet(self, name):
		grep = subprocess.Popen(('sudo apt-get install ' + name).split(), stdout=subprocess.PIPE).stdout.read()

	def getConf(self):
		return self.conf