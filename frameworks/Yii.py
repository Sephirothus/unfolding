from dists.Ubuntu import Ubuntu
from Helper import Helper
from servers.Apache import Apache
from servers.Nginx import Nginx

class Yii:

	dependencies = ['languages.Php', 'managers.Composer']
	name = 'Yii 2.0'

	version = ''
	folder = ''

	def getAttrs(self):
		self.version = self.attrs['version'] if hasattr(self, 'attrs') and 'version' in self.attrs else 'basic'
		self.folder = self.attrs['folder'] if hasattr(self, 'attrs') and 'folder' in self.attrs else '../yii-application'

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
				conf = apache.siteConf('admin.' + siteName, self.folder + '/backend/web') + "\n\n"
				conf += apache.siteConf(siteName, self.folder + '/frontend/web')
			else:
				conf = apache.siteConf(siteName, self.folder + '/web')

			apache.addSite(siteName, self.folder, conf)
		elif nginx.check():
			nginx.addSite(siteName, folder)

		if ['db', 'user', 'password'] in self.attrs:
			print 'yes'
		