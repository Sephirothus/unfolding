from Helper import Helper

from servers.Apache import Apache
from servers.Nginx import Nginx
from databases.Mysql import Mysql

class Yii:

	dependencies = ['languages.Php', 'managers.Composer']
	sortOrder = ["databases"]
	name = 'Yii 2.0'

	version = 'basic'
	folder = '/var/www/yii-application'
	siteName = 'yii.dev'
	server = False

	def getAttrs(self):
		apache = Apache()
		nginx = Nginx()
		if 'version' in self.attrs: self.version = self.attrs['version']
		if 'folder' in self.attrs: self.folder = self.attrs['folder']
		if 'siteName' in self.attrs: self.siteName = self.attrs['siteName']
		if apache.check(): 
			self.server = apache
		elif nginx.check():
			self.server = nginx

	def install(self):
		helper = Helper()
		self.getAttrs()
		helper.composerProject('yiisoft/yii2-app-' + self.version + ' ' + self.folder)
		# https://github.com/yiisoft/yii2/releases/download/2.0.6/yii-' + self.version + '-app-2.0.6.tgz
		if self.version == 'advanced':
			helper.execute('sudo php ' + self.folder + '/init --env="Development"')
			
	def configure(self):
		helper = Helper()
		self.getAttrs()

		print "-- Set chmod to runtime and assets"
		if self.version == 'advanced':
			helper.setChmod(['backend/assets/', 'backend/runtime/', 'backend/web/assets/', 'frontend/assets/', 'frontend/runtime/', 'frontend/web/assets/', 'console/runtime/'], self.folder)
		else:
			helper.setChmod(['assets/', 'runtime/'], self.folder)

		if self.version == 'advanced': path = {'admin' : self.folder + '/backend/web', '': self.folder + '/frontend/web'}
		else: path = self.folder + '/web'
		if self.server:
			print "-- Creating " + self.server.name + " config"
			helper.serverAddSite(self.server, self.siteName, path)

		if all (k in self.attrs for k in ['db', 'user', 'password']):
			if 'driver' in self.attrs:
				driver = self.attrs['driver']
			elif (Mysql()).check():
				driver = 'mysql'

			if self.version == 'advanced':
				print "-- Rewriting main-local config"
				dbFile = self.folder + '/common/config/main-local.php'
				dbConf = self.customConfFile(self.attrs['db'], self.attrs['user'], self.attrs['password'], driver)
			else:
				print "-- Rewriting db config"
				dbFile = self.folder + '/config/db.php'
				dbConf = '<?php\n return [\n' + self.customDbFile(self.attrs['db'], self.attrs['user'], self.attrs['password'], driver) + '];'

			helper.saveFile(dbFile, dbConf)

	def delete(self):
		helper = Helper()
		self.getAttrs()
		hosts = ['admin.' + self.siteName, self.siteName]
		print "-- Remove site folder"
		helper.rm(self.folder)

		if self.server:
			print "-- Remove " + self.server.name + " config"
			helper.serverRemoveSite(self.server, self.siteName, hosts)

	def customDbFile(self, db, user, password, driver='mysql'):
		return "\
'class' => 'yii\db\Connection',\n\
'dsn' => '" + driver + ":host=localhost;dbname=" + db + "',\n\
'username' => '" + user + "',\n\
'password' => '" + password + "',\n\
'charset' => 'utf8',\n\
'attributes'=>[\n\
	PDO::ATTR_PERSISTENT => true\n\
]\n"

	def customConfFile(self, db, user, password, driver='mysql'):
		return "<?php\n\
return [\n\
	'components' => [\n\
		'db' => [\n\
			" + self.customDbFile(db, user, password, driver) + "\
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
