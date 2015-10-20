import getpass

from dists.Ubuntu import Ubuntu
from Helper import Helper
from servers.Apache import Apache
from servers.Nginx import Nginx

class Yii:

	dependencies = ['languages.Php', 'managers.Composer']
	sortOrder = ["databases.Mysql", 'languages.Php', 'managers.Composer']
	name = 'Yii 2.0'

	version = ''
	folder = ''

	def getAttrs(self):
		self.version = self.attrs['version'] if hasattr(self, 'attrs') and 'version' in self.attrs else 'basic'
		self.folder = self.attrs['folder'] if hasattr(self, 'attrs') and 'folder' in self.attrs else '/home/' + getpass.getuser() + '/yii-application'

	def installUbuntu(self):
		myDist = Ubuntu()
		self.getAttrs()
		myDist.composerProject('yiisoft/yii2-app-' + self.version + ' ' + self.folder)
		if self.version == 'advanced':
			myDist.execute('sudo php ' + self.folder + '/init --env="Development"')
			
	def configure(self):
		self.getAttrs()
		apache = Apache()
		nginx = Nginx()
		siteName = self.attrs['siteName'] if 'siteName' in self.attrs else 'yii.dev'
		
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
			helper = Helper()
			confFolder = self.folder + '/' + ('common/config/' if self.version == 'advanced' else 'config/')
			hostName = helper.hostName()
			print "-- Creating custom configs folder"
			helper.execute('sudo mkdir ' + confFolder + hostName)
			print "-- Creating custom config with db"
			helper.saveFile(confFolder + hostName + '/custom-main.php', self.customConfFile(self.attrs['db'], self.attrs['user'], self.attrs['password']))
			print "-- Changing main config"
			helper.saveFile(confFolder + 'main.php', self.confFile())

	def customConfFile(self, db, user, password, driver='mysql'):
		return "<?php\
return [\
    'db' => [\
        'class' => 'yii\db\Connection',\
        'dsn' => '" + driver + ":host=localhost;dbname=" + db + "',\
        'username' => '" + user + "',\
        'password' => '" + password + "',\
        'charset' => 'utf8',\
        'attributes'=>[\
            PDO::ATTR_PERSISTENT => true\
        ]\
    ]\
];"

	def confFile(self):
		return "<?php\
$configFile = include __DIR__ . '/' . gethostname() . '/custom-main.php';\
\
$components = [\
	'cache' => [\
		'class' => 'yii\caching\FileCache',\
	],\
];\
$components = \yii\helpers\ArrayHelper::merge($components, $configFile);\
\
return [\
    'vendorPath' => dirname(dirname(__DIR__)) . '/vendor',\
    'components' => $components\
];"			
		