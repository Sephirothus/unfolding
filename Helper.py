import subprocess, shlex

class Helper:

	def execute(self, command):
		return subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE).stdout.read()
	
	def getClass(self, moduleName):
		className = moduleName.rsplit(".", 1)[1]
		moduleName = __import__(moduleName, fromlist=[className]);
		return getattr(moduleName, className)

	def objAdd(self, val, data):
		for i in data:
			if i.__class__.__name__ == val.__class__.__name__:
				return False    
		data.append(val)

	def ucfirst(self, string):
		return string[0].upper() + string[1:]

	def getDist(self, conf, onlyName=True):
		distName = ''
		if 'dists' in conf:
			distName = conf['dists']
		else:
			grep = self.execute("cat /etc/lsb-release")
			distName = grep.split('\n')[0].split('=')[1].lower()

		distName = self.ucfirst(distName)

		return distName if onlyName else self.getClass('dists.' + distName)()

	def createBlock(self, data):
		maxLen = len(max(data)) if type(data) is list else len(data)
		print "\n+" + ("=" * (maxLen+2)) + "+"

		if type(data) is list:
			for el in data:
				curLen = len(el)
				print "| " + el + (" " * (maxLen - curLen)) + " |"
		else:
			print "| " + data + " |"

		print "+" + ("=" * (maxLen+2)) + "+"

	def editFile(self, fileName, changes):
		fileData = open(fileName, "r+")
		newData = fileData.read()
		for oldVal, newVal in changes.iteritems():
			newData = newData.replace(oldVal, newVal)

		fileData.write(newData)
		fileData.close()

	def addHost(self, host):
		self.fileActions('/etc/hosts', 'a', '\n' + host)

	def saveFile(self, filePath, content):
		self.fileActions(filePath, 'w', content)

	def fileActions(self, fileName, mode, content):
		fileData = open(fileName, mode)
		fileData.write(content)
		fileData.close()

	def composerProject(self, params):
		return self.execute('sudo composer create-project --prefer-dist '+params)

	def mysqlCommand(self, command, user='root', password=False):
		return 'mysql -u ' + user + (' -p' + password if password else '') + ' -e "' + command + ';"'
