from dists.RouterDist import RouterDist

class Jdk(RouterDist):

	name = 'Jdk'

	downloadUrl = 'http://download.oracle.com/otn-pub/java/jdk/8u66-b17/jdk-8u66-linux-x64.tar.gz'
	folderName = 'oracle_jdk8'
	params = '--no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie"'
	paths = {
		'folderPath': '/usr/lib/jvm/',
		'pathFile': '/etc/profile.d/oraclejdk.sh',
		'jdkPath': '{$folderPath}jdk1.*'
	}
	conf = 'export J2SDKDIR={$folder}\n\
export J2REDIR={$folder}/jre\n\
export PATH=$PATH:{$folder}/bin:{$folder}/db/bin:{$folder}/jre/bin\n\
export JAVA_HOME={$folder}\n\
export DERBY_HOME={$folder}/db'
	
	def install(self):
		self.mkdir(self.paths['folderPath'])
		self.wgetUnpack(self.downloadUrl, self.paths['folderPath'], self.params)
		self.rename(self.paths['jdkPath'], self.paths['folderPath'] + self.folderName)
		self.saveFile(self.paths['pathFile'], self.conf.replace('{$folder}', self.paths['folderPath'] + self.folderName))
		self.execute('. ' + self.paths['pathFile'], True)

	def delete(self):
		self.rm([self.paths['folderPath'], self.paths['pathFile']])
		