import subprocess
import sys
import inspect
import importlib

class ConfigPaths:
	dependencies = {

	}

	dists = {
		'ubuntu': 'dists.Ubuntu',
		'opensuse': 'dists.OpenSuse',
		'fedora': 'dists.Fedora',
		'linux mint': 'dists.LinuxMint',
		'debian': 'dists.Debian',
		'gentoo': 'dists.Gentoo',
		'arch linux': 'dists.ArchLinux',
		'centos': 'dists.Centos',
		'mageia': 'dists.Mageia'
	}
	languages = {
		'php': 'languages.Php', 
		'ruby': 'languages.Ruby', 
		'python': 'languages.Python'
	}
	vcs = {
		'git': 'vcs.Git',
		'svn': 'vcs.Svn',
		'mercurial': 'vcs.Mercurial'
	}
	databases = {
		'mysql': ''
	}
	servers = {
		'php': {
			'apache': 'servers.Apache',
			'nginx': 'servers.Nginx'
		}
	}
	managers = {
		'php': {
			'composer': 'managers.Composer',
			'pear': 'managers.Pear',
		}
	}
	frameworks = {
		'php': {
			'codeigniter': 'frameworks.Codeigniter',
			'yii': 'frameworks.yii',
		}
	}

class Config:
	data = {}

	def makeConf(self, conf):
		newConf = []
		try:
			for key, val in conf.iteritems():
				var = getattr(ConfigPaths, key)
				if (type(var[var.keys()[0]]) is dict):
					newConf.append(var[conf['languages']][val])
				else:
					newConf.append(var[val])

			return newConf
		except:
			print sys.exc_info()

	def createConf(self):
		self.data['dist'] = self.setDist()
		self.data['language'] = self.setLang()
		self.data['server'] = self.setServer()
		# self.data['db'] = self.setDb()
		return self.getConf()

	def getConf(self):
		return self.data

	def getClass(self, moduleName):
		className = moduleName.rsplit(".", 1)[1]
		moduleName = __import__(moduleName, fromlist=[className]);
		return getattr(moduleName, className)

	def choice(self, arr, question, isRequired=False):
		string = '===== '+question+' =====\n'
		num = 0
		for key, val in arr.iteritems():
			string += str(num)+'. '+key+'\n'
			num += 1;

		if (isRequired is False): string += str(num)+'. Nothing\n'
		curChoice = raw_input(string+'Your choice? ')
		if (curChoice == str(num) and isRequired is False): print ''

		try:
			return arr.keys()[int(curChoice)]
		except:
			print 'not correct number'
			func = inspect.getouterframes(inspect.currentframe())[1][3]
			getattr(self, func)()



	def setDist(self):
		grep = subprocess.Popen(("cat /etc/lsb-release").split(), stdout=subprocess.PIPE).stdout.read()
		dist = grep.split('\n')[0].split('=')[1].lower()
		if (dist in self.dist): 
			return self.dist[dist]
		else:
			dist = raw_input('type your linux distribution name? ').lower()
			if (dist in self.dist): 
				return dist
			else:
				sys.exit('Sorry, this distribution does not supported:(')

	def setLang(self):
		choice = self.choice(ConfigPaths.languages, 'Select language? ')
		return ConfigPaths.languages[choice]

	def setServer(self):
		choice = self.choice(cl.servers, 'Select http server? ')
		return cl.servers[choice]

	def setVcs(self):
		return ''

	def setDb(self):
		choice = self.choice(self.languages, 'Select database? ')
		return self.languages[choice]
		