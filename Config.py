import subprocess
import sys
import inspect
import importlib

class Config:
	data = {}
	dist = {
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

	def makeConf(self):
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

	def choice(self, arr, question):
		string = '===== '+question+' =====\n'
		num = 0
		for key, val in arr.iteritems():
			string += str(num)+'. '+key+'\n'
			num += 1;
		curChoice = raw_input(string+'Your choice? ')

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
		choice = self.choice(self.languages, 'Select language? ')
		return self.languages[choice]

	def setServer(self):
		cl = self.getClass(self.data['language'])
		choice = self.choice(cl.servers, 'Select http server? ')
		return cl.servers[choice]

	def setDb(self):
		choice = self.choice(self.languages, 'Select database? ')
		return self.languages[choice]
		