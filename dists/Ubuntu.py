import subprocess

class Ubuntu:
	conf = {}

	def __init__(self, conf={}):
		self.conf = conf

	def execute(self, command):
		return subprocess.Popen((command).split(), stdout=subprocess.PIPE).stdout.read()

	def aptGet(self, name, rep=False):
		if rep:
			self.execute('sudo add-apt-repository ' + rep)
			self.execute('sudo apt-get update')

		print self.execute('sudo apt-get install -y ' + name)

	def install(self):
		return False