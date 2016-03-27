from Helper import Helper

class Laravel:

	dependencies = ['languages.Php', 'managers.Composer']
	sortOrder = ["databases"]
	name = 'Laravel 5'

	folder = '/var/www/laravel-application'

	def installUbuntu(self):
		if hasattr(self, 'attrs') and 'folder' in self.attrs: self.folder = self.attrs['folder']
		self.curDist.composerProject('laravel/laravel ' + self.folder)
		
	def configure(self):
		# TODO db config, apache|nginx config, hosts
		return False
