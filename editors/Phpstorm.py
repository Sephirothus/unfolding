from Helper import Helper
from dists.RouterDist import RouterDist

class Phpstorm(RouterDist):

	dependencies = ['extensions.Jdk']
	name = "PhpStorm"

	downloadUrl = 'http://download.jetbrains.com/webide/PhpStorm-9.0.2.tar.gz'

	def install(self):
		helper = Helper()
		folder = self.attrs['folder'] if hasattr(self, 'attrs') and 'folder' in self.attrs else helper.homeFolder()
		helper.wgetUnpack(self.downloadUrl, folder)
		# helper.execute(folder + 'PhpStorm-*/bin/phpstorm.sh', True)

	def delete(self):
		helper = Helper()
		folder = self.attrs['folder'] if hasattr(self, 'attrs') and 'folder' in self.attrs else helper.homeFolder()
		helper.rm(folder + 'PhpStorm-* ' + helper.homeFolder() + '.WebIde90')