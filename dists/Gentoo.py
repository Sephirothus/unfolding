from Helper import Helper

class Gentoo(Helper):

	def install(self, package, chosenVersion = False):
		if chosenVersion:
			package = '=' + package + '-' + chosenVersion
		return self.execute('sudo emerge ' + package)

	def delete(self, package):
		return self.execute('sudo emerge -cav ' + package)
