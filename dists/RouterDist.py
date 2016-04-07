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
		getattr(self, self.getMethod('beforeInstall', self))(package)
		self.currentDist.install(package['serviceName'], package['repository'], package['key'])
		getattr(self, self.getMethod('afterInstall', self))(package)

	def afterInstall(self, package):
		return False

	def check(self):
		if not hasattr(self, 'checkName'): raise Exception('Cannot check instance, no check method')
		return self.checkVersion(self.checkName)

	def beforeDelete(self, package):
		return False

	def delete(self):
		# TODO: add if not set version, then delete all versions
		package = self.__getPackage()
		getattr(self, self.getMethod('beforeDelete', self))(package)
		self.currentDist.delete(package['serviceName'] + '*', package['repository'], package['key'])
		getattr(self, self.getMethod('afterDelete', self))(package)

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
		package = {}
		if hasattr(self, 'packages'):
			distName = self.currentDist.__class__.__name__
			package = self.packages[distName] if distName in self.packages else self.packages

		if self.hasAttr(['packageAttr', 'defaultPackage', 'packages'], self):
			package = self.getPackageInfo(self.packageAttr, self.attrs, package, self.defaultPackage)
		elif not hasattr(self, 'packages'):
			package = self.getAttr(['serviceName', 'repository', 'key'], self)

		if 'repository' in package: package['repository'] = self.currentDist.getRelease(package['repository'])
		return package