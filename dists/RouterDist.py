from Helper import Helper

class RouterDist(Helper):

	# Reserved class attributes: packages, checkName, serviceName, dependencies, sortOrder, name

	# 'ubuntu', 'linuxmint', 'debian' - apt-get
	# 'opensuse' - zypper
	# 'fedora', 'centos' - yum
	# 'gentoo' - emerge
	# 'archlinux' - pacman
	# 'mageia' - urpmi
	supportedDists = ['ubuntu', 'linuxmint', 'debian', 'opensuse', 'fedora', 'gentoo', 'archlinux', 'centos', 'mageia']
	getOsCommand = "cat /etc/os-release"
	current = False

	def beforeInstall(self):
		return False

	def install(self):
		package = self.__getPackage()
		self.current.install(package['serviceName'], package['repository'], package['key'])

	def afterInstall(self):
		return False

	def check(self):
		if not hasattr(self, 'checkName'): raise Exception('Cannot check instance, no check method')
		return self.checkVersion(self.checkName)

	def beforeDelete(self):
		return False

	def delete(self):
		#self.current.delete(self.serviceName + '*')
		return False

	def afterDelete(self):
		return False

	def __getPackage(self):
		if hasattr(self, 'packageAttr') and hasattr(self, 'defaultPackage'):
			package = self.getPackageInfo(self.packageAttr, self.attrs, self.packages, self.defaultPackage)
		else:
			package = {
				'serviceName': self.getAttr('serviceName', self),
				'repository': self.getAttr('repository', self),
				'key': self.getAttr('key', self),
			}
		return package

	def getDist(self, conf = False):
		distName = ''
		if 'dists' in conf:
			distName = conf['dists']
		else:
			grep = self.execute(self.getOsCommand)
			distName = grep.split('\n')[0].split('=')[1].strip('"')

		if (distName.lower() not in self.supportedDists): raise Exception('Unknown or unsupported linux distributive')
		
		distName = self.ucfirst(distName.lower())
		self.current = self.getClass('dists.' + distName)()
		return self.current