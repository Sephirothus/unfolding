class Ubuntu:
	conf = {}

	def __init__(self, conf):
		self.conf = conf

	def install(self):
		print self.conf

	def getConf(self):
		return self.conf