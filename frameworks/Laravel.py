from dists.Ubuntu import Ubuntu

class Laravel:

	dependencies = ['languages.Php', 'managers.Composer']
	name = 'Laravel 5'

	def installUbuntu(self):
		myDist = Ubuntu()
		folder = self.attrs['folder'] if hasattr(self, 'attrs') and 'folder' in self.attrs else '../laravel-application'

		myDist.composerProject('laravel/laravel ' + folder)
		
	def configure(self):
		# TODO db config, apache|nginx config, hosts
		return False
