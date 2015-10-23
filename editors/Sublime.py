from dists.Ubuntu import Ubuntu

class Sublime:

	name = "Sublime Text"
	
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
		# package control https://packagecontrol.io/installation#ST3
		# add packages https://mattstauffer.co/blog/sublime-text-3-for-php-developers
		# packages: codeformatter, livereload, autocomplete, HTMLPrettify
		return False

	def checkUbuntu(self):
		ubuntu = Ubuntu()
		return ubuntu.checkAptGet('sublime-text-installer') or ubuntu.checkAptGet('sublime-text')
