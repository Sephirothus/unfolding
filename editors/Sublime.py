from dists.RouterDist import RouterDist

class Sublime(RouterDist):

	name = "Sublime Text"

	defaultPackage = '3'
	packageAttr = 'version'
	packages = {
		'Debian': {
			'2': {
				'serviceName': 'sublime-text',
				'repository': 'ppa:webupd8team/sublime-text-2'
			},
			'3': {
				'serviceName': 'sublime-text-installer',
				'repository': 'ppa:webupd8team/sublime-text-3'
			}
		}
	}
	paths = {
		'mainFolder': '{$homeFolder}.config/sublime-text-{$version}/',
		'installedPackagesFolder': '{$mainFolder}Installed\ Packages/',
		'packagesFolder': '{$mainFolder}Packages/',
		'userSettingsFolder': '{$mainFolder}Packages/User/'
	}

	def configure(self):
		self.setPaths({
			'homeFolder': self.homeFolder(), 
			'version': self.attrs['version'] if 'version' in self.attrs else self.defaultPackage
		})
		for name, package in self.getSublimePackages().iteritems():
			print '-- install package "' + name + '"'
			if type(package) is dict:
				if 'sublimeSupport' in package and 'version' in self.attrs and package['sublimeSupport'] != self.attrs['version']:
					print 'this package not supported by your version of Sublime Text'
					continue

				self.installPackage(package['url'])
				if 'settings' in package:
					settings = package['settings']
					if type(settings) is list:
						for el in settings:
							self.setSettings(el['fileName'], el['fileContent'])
					else: 
						self.setSettings(settings['fileName'], settings['fileContent'])
			else:
				self.installPackage(package)

		# package control https://packagecontrol.io/installation#ST3
		# add packages https://mattstauffer.co/blog/sublime-text-3-for-php-developers

	def checkDebian(self):
		for key, val in self.packages.iteritems():
			if self.currentDist.checkAptGet(val['serviceName']): return True
		return False

	def installPackage(self, packageUrl, packageType='packages'):
		folder = self.packagesFolder if packageType == 'packages' else self.installedPackagesFolder
		filePath = folder + '/' + packageUrl.rsplit('/', 1)[1]
		if not self.checkFile(filePath): self.wgetUnpack(packageUrl, folder)

	def setSettings(self, fileName, fileContent):
		self.fileActions(self.userSettingsFolder + fileName, 'a', fileContent)

	# sublime packages list
	def getSublimePackages(self):
		return {
			'Package Control': 'https://packagecontrol.io/Package%20Control.sublime-package',
			'PHP Companion': self.phpCompanionConf(),
			'All Autocomplete': 'https://github.com/alienhard/SublimeAllAutocomplete/archive/master.zip',
			'CodeFormatter': 'https://github.com/akalongman/sublimetext-codeformatter/archive/master.zip',
			'LiveReload': 'https://github.com/dz0ny/LiveReload-sublimetext2/archive/devel.zip',
			'HTML Prettify': 'https://github.com/victorporof/Sublime-HTMLPrettify/archive/master.zip',
			'SublimeCodeIntel': 'https://github.com/SublimeCodeIntel/SublimeCodeIntel/archive/master.zip',
			'PhpCodeGen': 'https://bitbucket.org/bteryek/phpcodegen/get/18c3d92b5a32.zip'
		}

	def phpCompanionConf(self):
		return {
			'url': 'https://github.com/erichard/SublimePHPCompanion/archive/master.zip',
			'settings': [{
				'fileName': 'Default (Linux).sublime-mousemap',
				'fileContent': '[\n\
	{\n\
		"button": "button1",\n\
		"count": 1,\n\
		"modifiers": ["ctrl"],\n\
		"press_command": "drag_select",\n\
		"command": "goto_definition"\n\
	}\n\
]'
			}, {
				'fileName': 'Default.sublime-keymap',
				'fileContent': '[\n\
	{ "keys": ["f6"], "command": "expand_fqcn" },\n\
	{ "keys": ["shift+f6"], "command": "expand_fqcn", "args": {"leading_separator": true} },\n\
	{ "keys": ["f5"], "command": "find_use" },\n\
	{ "keys": ["f4"], "command": "import_namespace" },\n\
	{ "keys": ["shift+f12"], "command": "goto_definition_scope" },\n\
	{ "keys": ["f7"], "command": "insert_php_constructor_property" }\n\
]'
			}],
			'sublimeSupport': '3'
		}
