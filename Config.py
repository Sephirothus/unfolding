import subprocess
import sys
import inspect

from Helper import Helper

class ConfigPaths:
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
	databases = [
		'mysql', 'postgresql', 'mongodb'
	]
	servers = {
		'apache': 'servers.Apache',
		'nginx': 'servers.Nginx'
	}
	managers = {
		'composer': 'managers.Composer',
		'pear': 'managers.Pear',
	}
	editors = [
		'phpshtorm', 'sublime'
	]
	frameworks = [
		'codeigniter', 'yii', 'laravel', 'phalcon', 'symfony', 'cakephp', 
		'zend', 'FuelPHP', 'kohana', 'phpixie', 'nette'
	]

class Config:

	data = {}
	helper = False
	argument = False

	def __init__(self, arg):
		self.argument = arg
		self.helper = Helper()

	def getConf(self):
		return self.data

	# =================== Checking ====================== #

	def createQueue(self, conf):
		queue = []
		try:
			for key, vals in conf.iteritems():
				if (type(vals) is list):
					for val in vals:
						self.checkDependencies(key, val, conf, queue)
				elif (type(vals) is dict):
					for name, params in vals.iteritems():
						self.checkDependencies(key, name, conf, queue, params)
				else:
					self.checkDependencies(key, vals, conf, queue)

			return self.sortQueue(queue)
		except:
			print sys.exc_info()

	def checkDependencies(self, folder, className, conf, queue, params=False):
		curClass = self.helper.getClass(folder + '.' + self.helper.ucfirst(className))()
		if hasattr(curClass, 'dependencies') and self.argument == 'install':
			for val in curClass.dependencies:
				curVal = val.split('.')
				if curVal[0] in conf:
					if curVal[1] == conf[curVal[0]] or (hasattr(conf[curVal[0]], 'keys') and curVal[1] in conf[curVal[0]].keys()):
						continue

				self.checkDependencies(curVal[0], curVal[1], conf, queue)

		if params:
			curClass.attrs = {}
			for key, val in params.iteritems():
				curClass.attrs[key] = val
		self.helper.listAdd(curClass, queue)

	def sortQueue(self, queue):
		newQueue = []
		for val in queue:
			if hasattr(val, 'sortOrder'):
				for sortEl in val.sortOrder:
					foundVal = self.helper.listFind(sortEl, queue)
					if foundVal: self.helper.listAdd(foundVal, newQueue)
				self.helper.listAdd(val, newQueue)

		self.helper.listMerge(queue, newQueue)
		return newQueue

	# =================== Creation ====================== #

	def createConf(self):
		self.data['dist'] = self.setDist()
		self.data['language'] = self.setLang()
		self.data['server'] = self.setServer()
		# self.data['db'] = self.setDb()
		return self.getConf()

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
		grep = self.helper.execute("cat /etc/lsb-release")
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
		