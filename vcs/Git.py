from Helper import Helper
from dists.RouterDist import RouterDist

class Git(RouterDist):

	name = "Git"
	serviceName = 'git'

	def installUbuntu(self):
		print self.currentDist.aptGet(self.serviceName)

	def deleteUbuntu(self):
		return self.currentDist.removeAptGet(self.serviceName)

	def check(self):
		return (Helper()).checkVersion(self.serviceName)
		
	def configure(self):
		helper = Helper()
		if not helper.checkFile('/etc/bash_completion.d/git-completion.bash'):
			print "-- add bash completion"
			helper.wget('https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash', '/etc/bash_completion.d/')

		if 'name' in self.attrs:
			print "-- set your name in git config"
			helper.execute('git config --global user.name "' + self.attrs['name'] + '"')

		if 'email' in self.attrs:
			fileName = helper.homeFolder() + '.ssh/id_rsa'
			print "-- set your email in git config"
			helper.execute('git config --global user.email "' + self.attrs['email'] + '"')
			if 'passphrase' in self.attrs and len(self.attrs['passphrase']) > 4:
				print "-- create ssh key for auto-authorization (add string below to https://github.com/settings/ssh)"
				if not helper.checkFile(fileName):
					helper.execute('mkdir ' + helper.homeFolder() + '.ssh')
					helper.execute('ssh-keygen -f "' + fileName + '" -N "' + self.attrs['passphrase'] + '" -t rsa -C "' + self.attrs['email'] + '"')
				print helper.execute('cat ' + fileName + '.pub')
