from Helper import Helper

class Jdk:

	name = 'Jdk'

	downloadUrl = 'http://download.oracle.com/otn-pub/java/jdk/8u66-b17/jdk-8u66-linux-x64.tar.gz'
	folderPath = '/usr/lib/jvm/'
	folderName = 'oracle_jdk8'
	pathFile = '/etc/profile.d/oraclejdk.sh'
	params = '--no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie"'
	
	def install(self):
		helper = Helper()
		helper.execute('mkdir ' + self.folderPath)
		helper.wgetUnpack(self.downloadUrl, self.folderPath, self.params)
		helper.execute('sudo mv ' + self.folderPath + 'jdk1.* ' + self.folderPath + self.folderName, True)
		helper.saveFile(self.pathFile, self.getPathContent())
		helper.execute('. ' + self.pathFile, True)

	def delete(self):
		(Helper()).rm(self.folderPath + ' ' + self.pathFile)
		
	def getPathContent(self):
		folder = self.folderPath + self.folderName
		return 'export J2SDKDIR=' + folder + '\n\
export J2REDIR=' + folder + '/jre\n\
export PATH=$PATH:' + folder + '/bin:' + folder + '/db/bin:' + folder + '/jre/bin\n\
export JAVA_HOME=' + folder + '\n\
export DERBY_HOME=' + folder + '/db'