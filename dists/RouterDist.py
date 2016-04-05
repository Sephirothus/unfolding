import re
from Helper import Helper

class RouterDist(Helper):

	# Reserved class attributes: packages, checkName, serviceName, dependencies, sortOrder, name

	# 'ubuntu', 'linuxmint', 'debian' - apt-get
	# 'opensuse' - zypper
	# 'fedora', 'centos' - yum
	# 'gentoo' - emerge
	# 'archlinux' - pacman
	# 'mageia' - urpmi
	supportedDists = {
		'Debian': ['ubuntu', 'linuxmint', 'debian'],
		'Redhat': ['fedora', 'centos linux'], 
		'Archlinux': ['archlinux'],
		'Gentoo': ['gentoo'],
		'Opensuse': ['opensuse'],
		'Mageia': ['mageia']
	}
	getOsCommand = "cat /etc/os-release"
	currentDist = False

	def beforeInstall(self, package):
		return False

	def install(self):
		package = self.__getPackage()
		self.beforeInstall(package)
		self.currentDist.install(package['serviceName'], package['repository'], package['key'])
		self.afterInstall(package)

	def afterInstall(self, package):
		return False

	def check(self):
		if not hasattr(self, 'checkName'): raise Exception('Cannot check instance, no check method')
		return self.checkVersion(self.checkName)

	def beforeDelete(self, package):
		return False

	def delete(self):
		# add if not set version, then delete all versions
		package = self.__getPackage()
		self.beforeDelete(package)
		self.currentDist.delete(package['serviceName'] + '*', package['repository'], package['key'])
		self.afterDelete(package)
		return False

	def afterDelete(self, package):
		return False

	def getDist(self, conf = False):
		distName = ''
		if 'dists' in conf:
			distName = conf['dists']
		else:
			distName = re.search('ID=(\S+)', self.execute(self.getOsCommand)).group(1).strip('"')

		distGroup = False
		for key, dist in self.supportedDists.iteritems(): 
			if distName.lower() in dist: distGroup = key

		if not distGroup: raise Exception('Unknown or unsupported linux distribution')
		
		self.currentDist = self.getClass('dists.' + distGroup)()
		return self.currentDist

	def __getPackage(self):
		if self.hasAttr(['packageAttr', 'defaultPackage', 'packages'], self):
			package = self.getPackageInfo(self.packageAttr, self.attrs, self.packages, self.defaultPackage)
		else:
			package = self.getAttr(['serviceName', 'repository', 'key'], self)
		package['repository'] = self.getLsbRelease(package['repository'])
		return package