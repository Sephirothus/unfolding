from Helper import Helper

class Sublime:

	name = "Sublime Text"

	mainFolder = '{$home_folder}.config/sublime-text-{$version}/'
	installedPackagesFolder = '{$main_folder}Installed\ Packages/'
	packagesFolder = '{$main_folder}Packages/'
	userSettingsFolder = '{$main_folder}Packages/User/'

	defaultPackage = '3'
	packages = {
		'2': {
			'command': 'sublime-text',
			'rep': 'ppa:webupd8team/sublime-text-2'
		},
		'3': {
			'command': 'sublime-text-installer',
			'rep': 'ppa:webupd8team/sublime-text-3'
		}
	}
	
	def installUbuntu(self):
		package = self.curDist.getPackageInfo('version', self.attrs, self.packages, self.defaultPackage)
		self.curDist.aptGet(package['command'], package['rep'])

	def configure(self):
		self.setPaths()
		for name, package in self.getPackages().iteritems():
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

	def checkUbuntu(self):
		for key, val in self.packages.iteritems():
			if self.curDist.checkAptGet(val['command']): return True
		return False

	def setPaths(self):
		self.mainFolder = self.mainFolder.replace('{$home_folder}', (Helper()).homeFolder())
		self.mainFolder = self.mainFolder.replace('{$version}', self.attrs['version'] if 'version' in self.attrs else self.defaultPackage)
		self.installedPackagesFolder = self.installedPackagesFolder.replace('{$main_folder}', self.mainFolder)
		self.packagesFolder = self.packagesFolder.replace('{$main_folder}', self.mainFolder)
		self.userSettingsFolder = self.userSettingsFolder.replace('{$main_folder}', self.mainFolder)

	def installPackage(self, packageUrl, packageType='packages'):
		helper = Helper()
		folder = self.packagesFolder if packageType == 'packages' else self.installedPackagesFolder
		filePath = folder + '/' + packageUrl.rsplit('/', 1)[1]
		if not helper.checkFile(filePath): helper.wgetUnpack(packageUrl, folder)

	def setSettings(self, fileName, fileContent):
		(Helper()).fileActions(self.userSettingsFolder + fileName, 'a', fileContent)

	# sublime packages list
	def getPackages(self):
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
