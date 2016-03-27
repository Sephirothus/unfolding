from os.path import expanduser
import subprocess, shlex, socket, os.path, inspect

class Helper:

	supportedDists = ['ubuntu', 'opensuse', 'fedora', 'linuxmint', 'debian', 'gentoo', 'archlinux', 'centos', 'mageia']
	logFileName = 'commands.log'

	def execute(self, command, withShell=False):
		rawCommand = command
		if not withShell:
			command = shlex.split(command)
		output = subprocess.Popen(command, shell=withShell, stdout=subprocess.PIPE).stdout.read()
		# log command and it's output
		self.fileActions(self.logFileName, 'a', '>>>>> ' + rawCommand + "\n" + output)
		return output
	
	def getClass(self, moduleName):
		className = moduleName.rsplit(".", 1)[1]
		moduleName = __import__(moduleName, fromlist=[className]);
		return getattr(moduleName, className)

	# list of objects actions
	def listAdd(self, val, data):
		for i in data:
			if i.__class__.__name__ == val.__class__.__name__:
				return False    
		data.append(val)

	def listMerge(self, vals, data):
		for val in vals:
			self.listAdd(val, data)

	def listFind(self, val, data):
		className = val.split('.')
		for i in data:
			if len(className) == 1:
				folder = inspect.getfile(i.__class__).split('/')[-2]
				if folder == className[0]:
					return i
			elif len(className) == 2 and i.__class__.__name__ == className[1]:
				return i

	def mergeDicts(self, first, second):
		data = first.copy()
		data.update(second)
		return data

	def ucfirst(self, string):
		return string[0].upper() + string[1:]

	def getDist(self, conf=False, onlyName=False):
		distName = ''
		if 'dists' in conf:
			distName = conf['dists']
		else:
			grep = self.execute("cat /etc/os-release")
			distName = grep.split('\n')[0].split('=')[1].strip('"')

		if (distName.lower() not in self.supportedDists): raise Exception('Unknown or unsupported linux distributive')
		
		distName = self.ucfirst(distName.lower())
		return distName if onlyName else self.getClass('dists.' + distName)()

	def hostName(self):
		return socket.gethostname()

	def homeFolder(self):
		return expanduser("~") + '/'

	def createBlock(self, data):
		maxLen = max(len(s) for s in data) if type(data) is list else len(data)
		print "\n+" + ("=" * (maxLen+2)) + "+"

		if type(data) is list:
			for el in data:
				curLen = len(el)
				print "| " + el + (" " * (maxLen - curLen)) + " |"
		else:
			print "| " + data + " |"

		print "+" + ("=" * (maxLen+2)) + "+"

	def wget(self, filePath, folder, params=''):
		fileName = filePath.rsplit('/', 1)[1]
		self.execute('wget -P ' + folder + ' ' + filePath + ' ' + params)
		return folder.rstrip('/') + '/' + fileName

	def wgetUnpack(self, filePath, destination='/tmp', params=''):
		fileName = filePath.rsplit('/', 1)[1]
		fileExt = fileName.rsplit('.', 1)[1]
		
		self.wget(filePath, '/tmp', params)
		if fileExt == 'gz':
			self.execute('tar xvzf /tmp/' + fileName + ' -C ' + destination)
		elif fileExt == 'zip':
			self.execute('unzip /tmp/' + fileName + ' -d ' + destination)

		self.rm('/tmp/' + fileName)

	def dpkg(self, filePath):
		self.execute('dpkg -i ' + filePath)

	def wgetDpkg(self, filePath):
		file = self.wget(filePath, '/tmp')
		self.dpkg(file)
		self.rm(file)

	def editFile(self, fileName, changes):
		fileData = open(fileName, "r")
		newData = fileData.read()
		fileData.close()
		for oldVal, newVal in changes.iteritems():
			newData = newData.replace(oldVal, newVal)

		fileData = open(fileName, "w")
		fileData.write(newData)
		fileData.close()

	def addHost(self, host):
		self.fileActions('/etc/hosts', 'a', '\n' + host)

	def removeHost(self, hosts):
		self.editFile('/etc/hosts', {i: '' for i in hosts})

	def saveFile(self, filePath, content):
		self.fileActions(filePath, 'w', content)

	def fileActions(self, fileName, mode, content):
		fileData = open(fileName, mode)
		fileData.write(content)
		fileData.close()

	def rm(self, files):
		self.execute('sudo rm -rf ' + files, True)

	def checkFile(self, fileName):
		return os.path.isfile(fileName)

	def composerProject(self, params):
		return self.execute('sudo composer create-project --prefer-dist ' + params)

	def mysqlCommand(self, command, user='root', password='1'):
		return self.execute('mysql -u ' + user + (' -p' + password if password else '') + ' -e "' + command + ';"')

	def postgreCommand(self, command, user='postgres', password='postgres'):
		return self.execute('psql -U ' + user + (' -W' + password if password else '') + ' -c "' + command + ';"')

	def setChmod(self, files, folder=''):
		if folder: folder += '/'
		paths = ''
		if type(files) is list:
			for f in files:
				paths += folder + f + ' '
		else:
			paths += folder + files

		return self.execute('sudo chmod -R 777 ' + paths)

	def debConfSetSelections(self, params):
		if type(params) != str: params = '\n'.join(params)
		self.execute('echo "' + params + '" | sudo debconf-set-selections', True)

	def getLsbRelease(self):
		return self.execute('lsb_release -sc').strip()

	def checkVersion(self, service, versCom = '--version'):
		try:
			self.execute(service + ' ' + versCom)
			return True
		except OSError:
			return False

	def getMethod(self, method, obj, distName=False):
		methodName = False
		if not distName:
			distName = self.getDist()
			
		if method + distName in dir(obj):
			methodName = method + distName
		elif method in dir(obj):
			methodName = method

		return methodName

	def execMethod(self, method, obj, params = False):
		if method in dir(obj):
			return getattr(obj, method)(params)
		return False

	# server (apache, nginx) actions
	def serverAddSite(self, server, siteName, folder):
		config = ''
		host = ''
		# if folder is dictionary, then keys are aliases and values are paths
		if (type(folder) is dict):
			for alias, path in folder.iteritems():
				site = alias + '.' + siteName if alias else siteName
				config += server.siteConf(site, path) + "\n\n"
				host += '127.0.0.1	' + site + "\n"
		else:
			config = server.siteConf(siteName, folder)
			host = '127.0.0.1	' + siteName

		siteName += '.conf'
		path = server.path + siteName

		print "-- Save config file for server"
		self.saveFile(path, config)
		print "-- Enabling site"
		server.enableSite(siteName)
		print "-- Restart service"
		server.restart()
		print "-- Add site to hosts"
		self.addHost(host)

	def serverRemoveSite(self, server, siteName, hosts):
		siteName += '.conf'
		print "-- Remove server site link"
		self.execute('sudo rm ' + server.path + siteName)
		print "-- Disable server site"
		server.disableSite(siteName)
		print "-- Restart service"
		server.restart()
		print "-- Remove hosts"
		for key, val in enumerate(hosts):
			hosts[key] = '127.0.0.1	' + val
		self.removeHost(hosts)
