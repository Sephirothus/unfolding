from dists.RouterDist import RouterDist

from servers.Apache import Apache
from servers.Nginx import Nginx
from databases.Mysql import Mysql

class Yii(RouterDist):

	dependencies = ['languages.Php', 'managers.Composer']
	sortOrder = ["databases", "servers"]
	name = 'Yii 2.0'

	composerPath = 'yiisoft/yii2-app-{$version}'
	defaultPackage = 'basic'
	packageAttr = 'version'
	driver = 'mysql'
	folder = '/var/www/yii-application'
	siteName = 'yii.dev'
	server = False
	packages = {
		'basic': {
			'folders': ['assets/', 'runtime/'],
			'path': '{$proj_folder}/web',
			'confFile': '{$proj_folder}/config/db.php'
		},
		'advanced': {
			'folders': [
				'backend/assets/', 'backend/runtime/', 'backend/web/assets/', 'frontend/assets/', 
				'frontend/runtime/', 'frontend/web/assets/', 'console/runtime/'
			],
			'path': {'admin' : '{$proj_folder}/backend/web', '': '{$proj_folder}/frontend/web'},
			'confFile': '{$proj_folder}/common/config/main-local.php'
		}
	}

	def install(self):
		package = self.getPackage()
		if not self.isFolderNotEmpty(self.folder) or self.question("Current folder " + self.folder + " is not empty. Remove it?"):
			self.rm(self.folder)
			self.composerProject(self.composerPath.replace('{$version}', package['__index']) + ' ' + self.folder)
			self.execPackageMethod('install', self, package)
			
	def configure(self):
		package = self.getPackage()

		print "-- Set chmod to runtime and assets"
		self.setChmod(package['folders'], self.folder)

		if self.server:
			print "-- Creating " + self.server.name + " config"
			self.serverAddSite(self.server, self.siteName, package['path'])

		if all (k in self.attrs for k in ['db', 'user', 'password']):
			dbConf = self.currentDist.execPackageMethod('getConf', self, package)
			self.saveFile(package['confFile'], dbConf)

	def check(self):
		return False

	def delete(self):
		package = self.getPackage()
		hosts = ['admin.' + self.siteName, self.siteName]
		print "-- Remove site folder"
		self.rm(self.folder)

		if self.server:
			print "-- Remove " + self.server.name + " config"
			self.serverRemoveSite(self.server, self.siteName, hosts)

	def getPackage(self):
		apache = Apache()
		nginx = Nginx()
		package = self.getPackageInfo(self.packageAttr, self.attrs, self.packages, self.defaultPackage)
		if 'folder' in self.attrs: self.folder = self.attrs['folder']
		if 'siteName' in self.attrs: self.siteName = self.attrs['siteName']
		if 'driver' in self.attrs: self.driver = self.attrs['driver']
		if apache.check(): 
			self.server = apache
		elif nginx.check():
			self.server = nginx
		
		package['confFile'] = package['confFile'].replace('{$proj_folder}', self.folder)
		if type(package['path']) is dict:
			for key, val in package['path'].iteritems():
				package['path'][key] = package['path'][key].replace('{$proj_folder}', self.folder)
		else:
			package['path'] = package['path'].replace('{$proj_folder}', self.folder)
		return package

	def advancedInstall(self, data):
		(Helper()).execute('sudo php ' + self.folder + '/init --env="Development"')

	def basicGetConf(self, data):
		print "-- Rewriting db config"
		return '<?php\n return [\n' + self.customDbFile() + '];'

	def advancedGetConf(self, data):
		print "-- Rewriting main-local config"
		return self.customConfFile()

	def customDbFile(self):
		return "\
'class' => 'yii\db\Connection',\n\
'dsn' => '" + self.driver + ":host=localhost;dbname=" + self.attrs['db'] + "',\n\
'username' => '" + self.attrs['user'] + "',\n\
'password' => '" + self.attrs['password'] + "',\n\
'charset' => 'utf8',\n\
'attributes'=>[\n\
	PDO::ATTR_PERSISTENT => true\n\
]\n"

	def customConfFile(self):
		return "<?php\n\
return [\n\
	'components' => [\n\
		'db' => [\n\
			" + self.customDbFile() + "\
		],\n\
		'mailer' => [\n\
			'class' => 'yii\swiftmailer\Mailer',\n\
			'viewPath' => '@common/mail',\n\
			// send all mails to a file by default. You have to set\n\
			// 'useFileTransport' to false and configure a transport\n\
			// for the mailer to send real emails.\n\
			'useFileTransport' => true,\n\
		],\n\
	],\n\
];"
