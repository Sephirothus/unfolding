from dists.Ubuntu import Ubuntu

class Yii:

	dependencies = ['languages.Php', 'managers.Composer']
	name = 'Yii 2.0'

	def installUbuntu(self):
		myDist = Ubuntu()
		version = self.attrs['version'] if hasattr(self, 'attrs') and 'version' in self.attrs else 'basic'
		folder = self.attrs['folder'] if hasattr(self, 'attrs') and 'folder' in self.attrs else '../yii-application'

		myDist.composerProject('yiisoft/yii2-app-' + version + ' ' + folder)
		if version == 'advanced':
			myDist.execute('php ' + folder + '/init')
			
		# TODO db config, apache|nginx config, hosts