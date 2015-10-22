from dists.Ubuntu import Ubuntu
from Helper import Helper

from servers.Apache import Apache
from servers.Nginx import Nginx
from databases.Mysql import Mysql

class Yii:

	dependencies = ['languages.Php', 'managers.Composer']
	sortOrder = ["databases.Mysql", 'languages.Php', 'managers.Composer']
	name = 'Yii 2.0'

	version = ''
	folder = ''

	def getAttrs(self):
		self.version = self.attrs['version'] if hasattr(self, 'attrs') and 'version' in self.attrs else 'basic'
		self.folder = self.attrs['folder'] if hasattr(self, 'attrs') and 'folder' in self.attrs else (Helper()).homeFolder() + 'yii-application'

	def installUbuntu(self):
		myDist = Ubuntu()
		self.getAttrs()
		myDist.composerProject('yiisoft/yii2-app-' + self.version + ' ' + self.folder)
		if self.version == 'advanced':
			myDist.execute('sudo php ' + self.folder + '/init --env="Development"')
			
	def configure(self):
		self.getAttrs()
		helper = Helper()
		apache = Apache()
		nginx = Nginx()
		siteName = self.attrs['siteName'] if 'siteName' in self.attrs else 'yii.dev'

		print "-- Set chmod to runtime and assets"
		if self.version == 'advanced':
			helper.setChmod(['backend/assets/', 'backend/runtime/', 'backend/web/assets/', 'frontend/assets/', 'frontend/runtime/', 'frontend/web/assets/', 'console/runtime/'], self.folder)
		else:
			helper.setChmod(['assets/', 'runtime/'], self.folder)

		if apache.check():
			if self.version == 'advanced':
				apache.addSiteWithAliases(siteName, {
					'admin' : self.folder + '/backend/web',
					'': self.folder + '/frontend/web'
				})
			else:
				apache.addSite(siteName, self.folder + '/web')
		elif nginx.check():
			nginx.addSite(siteName, self.folder)

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
