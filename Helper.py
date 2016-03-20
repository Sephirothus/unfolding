from os.path import expanduser
import subprocess, shlex, socket, os.path, inspect

class Helper:

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

	def ucfirst(self, string):
		return string[0].upper() + string[1:]

	def getDist(self, conf=False, onlyName=True):
		distName = ''
		if 'dists' in conf:
			distName = conf['dists']
		else:
			grep = self.execute("cat /etc/lsb-release")
			distName = grep.split('\n')[0].split('=')[1].lower()

		distName = self.ucfirst(distName)

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
		return 'mysql -u ' + user + (' -p' + password if password else '') + ' -e "' + command + ';"'

	def postgreCommand(self, command, user='postgres', password='postgres'):
		return 'psql -U ' + user + (' -W' + password if password else '') + ' -c "' + command + ';"'

	def setChmod(self, files, folder=''):
		if folder: folder += '/'
		paths = ''
		if type(files) is list:
			for f in files:
				paths += folder + f + ' '
		else:
			paths += folder + files

		return self.execute('sudo chmod -R 777 ' + paths)

	def checkVersion(self, service):
		try:
			self.execute(service + ' --version')
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
