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
	defaultAttrNames = ['serviceName', 'repository', 'key']
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
		if hasattr(self, 'packageAttr') and self.packageAttr in self.attrs:
			self.__deleteActions(self.__getPackage())
		else: 
			packages = self.__getPackagesForCurDist()
			if not packages: packages = self.__getPackage()

			if 'serviceName' in packages:
				self.__deleteActions(self.__getCompletePackageInfo(packages))
			else:
				for key, val in packages.iteritems():
					self.__deleteActions(self.__getCompletePackageInfo(val, key))

	def afterDelete(self, package):
		return False

	def __deleteActions(self, package):
		getattr(self, self.getMethod('beforeDelete', self))(package)
		self.currentDist.delete(package['serviceName'] + '*', package['repository'])
		getattr(self, self.getMethod('afterDelete', self))(package)

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
		package = self.__getPackagesForCurDist()

		if self.hasAttr(['packageAttr', 'defaultPackage', 'packages'], self):
			package = self.getPackageInfo(self.packageAttr, self.attrs, package, self.defaultPackage)
		elif not hasattr(self, 'packages'):
			package = self.getAttr(self.defaultAttrNames, self)

		package = self.__getCompletePackageInfo(package)

		if package['repository']: package['repository'] = self.currentDist.getRelease(package['repository'])
		if not package['serviceName']: raise Exception('No serviceName in package data')
		return package

	def __getPackagesForCurDist(self):
		packages = {}
		if hasattr(self, 'packages') and self.currentDist:
			checkDists = dict((key.lower(), val) for key, val in self.packages.iteritems())
			distName = self.currentDist.__class__.__name__.lower()
			packages = checkDists[distName] if distName in checkDists else self.packages

		return packages

	def __getCompletePackageInfo(self, package, indexName = False):
		if indexName: package['__index'] = indexName
		return self.mergeDicts(package, self.getAttr(self.defaultAttrNames, package))