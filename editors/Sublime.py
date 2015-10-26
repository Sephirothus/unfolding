from dists.Ubuntu import Ubuntu
from Helper import Helper

class Sublime:

	name = "Sublime Text"

	mainFolder = ''
	installedPackagesFolder = ''
	packagesFolder = ''
	packages = {
		'Package Control': 'https://packagecontrol.io/Package%20Control.sublime-package',
		'PHP Companion': self.phpCompanionConf(),
		'All Autocomplete': 'https://github.com/alienhard/SublimeAllAutocomplete/archive/master.zip',
		'CodeFormatter': 'https://github.com/akalongman/sublimetext-codeformatter/archive/master.zip',
		'LiveReload': 'https://github.com/dz0ny/LiveReload-sublimetext2/archive/devel.zip',
		'HTML Prettify': 'https://github.com/victorporof/Sublime-HTMLPrettify/archive/master.zip',
		'SublimeCodeIntel': 'https://github.com/SublimeCodeIntel/SublimeCodeIntel/archive/master.zip',
		'PhpCodeGen': 'https://bitbucket.org/bteryek/phpcodegen/get/18c3d92b5a32.zip'
	}
	
	def installUbuntu(self):
		command = 'sublime-text-installer'
		rep = 'ppa:webupd8team/sublime-text-3'
		if hasattr(self, 'attrs'):
			if 'version' in self.attrs:
				version = self.attrs['version']
				if version == '2':
					command = 'sublime-text'
					rep = 'ppa:webupd8team/sublime-text-2'

		print (Ubuntu()).aptGet(command, rep)

	def configure(self):
		self.setPaths()
		for name, package in self.packages.iteritems():
			print '-- install package "' + name + '"'
			if type(package) is dict:
				if 'sublimeSupport' in package and 'version' in self.attrs and package['sublimeSupport'] != self.attrs['version']:
					print 'this package not supported by your version of Sublime Text'
					continue

				self.getPackage(package['url'])
				if 'settings' in package:
					settings = package['settings']
					if type(settings) is list:
						for el in settings:
							self.setSettings(el['fileName'], el['fileContent'])
					else: 
						self.setSettings(settings['fileName'], settings['fileContent'])
			else:
				self.getPackage(package)

		# package control https://packagecontrol.io/installation#ST3
		# add packages https://mattstauffer.co/blog/sublime-text-3-for-php-developers

	def checkUbuntu(self):
		ubuntu = Ubuntu()
		return ubuntu.checkAptGet('sublime-text-installer') or ubuntu.checkAptGet('sublime-text')

	def setPaths(self):
		helper = Helper()
		self.mainFolder = helper.homeFolder() + '.config/sublime-text-' + (self.attrs['version'] if 'version' in self.attrs else '3') + '/'
		self.installedPackagesFolder = self.mainFolder + 'Installed\ Packages/'
		self.packagesFolder = self.mainFolder + 'Packages/'

	def getPackage(self, packageUrl, packageType='packages'):
		helper = Helper()
		folder = self.packagesFolder if packageType == 'packages' else self.installedPackagesFolder
		filePath = folder + '/' + packageUrl.rsplit('/', 1)[1]
		if not helper.checkFile(filePath): helper.wgetUnpack(packageUrl, folder)

	def setSettings(self, fileName, fileContent):
		helper = Helper()
		helper.fileActions(self.mainFolder + 'Packages/User/' + fileName, 'a', fileContent)

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
