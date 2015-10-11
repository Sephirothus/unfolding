class Laravel:

	dependencies = ['languages.Php', 'managers.Composer']

	def install(self, myDist):
		myDist.createBlock("Installing Laravel 5")
		folder = self.attrs['folder'] if hasattr(self, 'attrs') and 'folder' in self.attrs else '../laravel-application'

		myDist.composerProject('laravel/laravel ' + folder)
		
		# TODO db config, apache|nginx config, hosts
