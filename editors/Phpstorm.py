from Helper import Helper

class Phpstorm:

	dependencies = ['extensions.Jdk']
	name = "PhpStorm"

	def install(self):
		helper = Helper()
		folder = self.attrs['folder'] if hasattr(self, 'attrs') and 'folder' in self.attrs else helper.homeFolder()
		helper.wgetUnpack('http://download.jetbrains.com/webide/PhpStorm-9.0.2.t..', folder)
		# helper.execute(folder + 'PhpStorm-*/bin/phpstorm.sh', True)

	def delete(self):
		helper = Helper()
		folder = self.attrs['folder'] if hasattr(self, 'attrs') and 'folder' in self.attrs else helper.homeFolder()
		helper.execute('sudo rm -rf ' + folder + 'PhpStorm-* ' + helper.homeFolder() + '.WebIde90')