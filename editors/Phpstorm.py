from dists.RouterDist import RouterDist

class Phpstorm(RouterDist):

	dependencies = ['extensions.Jdk']
	name = "PhpStorm"

	downloadUrl = 'http://download.jetbrains.com/webide/PhpStorm-9.0.2.tar.gz'
	packageFolder = 'PhpStorm-*'
	settingsFolder = '.WebIde90'

	def install(self):
		self.wgetUnpack(self.downloadUrl, self.getFolder())
		# helper.execute(folder + 'PhpStorm-*/bin/phpstorm.sh', True)

	def delete(self):
		self.rm([self.getFolder() + self.packageFolder, self.homeFolder() + self.settingsFolder])

	def getFolder(self):
		return (self.attrs['folder'] if hasattr(self, 'attrs') and 'folder' in self.attrs else self.homeFolder()).rstrip('/') + '/'