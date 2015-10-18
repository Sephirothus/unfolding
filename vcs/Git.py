from dists.Ubuntu import Ubuntu
from Helper import Helper

class Git:

	name = "Git"

	def installUbuntu(self):
		ubuntu = Ubuntu()
		ubuntu.execute('wget -P /etc/bash_completion.d/ https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash')
		print ubuntu.aptGet('git')

	def check(self):
		return (Helper()).checkVersion('git')
		