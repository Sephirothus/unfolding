from dists.Ubuntu import Ubuntu
from Helper import Helper

class Git:

	name = "Git"

	def installUbuntu(self):
		print (Ubuntu()).aptGet('git')

	def check(self):
		return (Helper()).checkVersion('git')
		
	def configure(self):
		helper = Helper()
		print "-- add bash completion"
		helper.wget('https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash', '/etc/bash_completion.d/')

		if 'name' in self.attrs:
			print "-- set your name in git config"
			helper.execute('git config --global user.name "' + self.attrs['name'] + '"')

		if 'email' in self.attrs:
			fileName = helper.homeFolder() + '.ssh/id_rsa'
			print "-- set your email in git config"
			helper.execute('git config --global user.email "' + self.attrs['email'] + '"')
			if 'passphrase' in self.attrs:
				print "-- create ssh key for auto-authorization (add string below to https://github.com/settings/ssh)"
				if not helper.checkFile(fileName):
					helper.execute('ssh-keygen -f "' + fileName + '" -N "' + self.attrs['passphrase'] + '" -t rsa -C "' + self.attrs['email'] + '"')
				print helper.execute('cat ' + fileName + '.pub')
