from dists.RouterDist import RouterDist

class Redis(RouterDist):

	name = 'Redis'

	checkName = 'redis-server'
	serviceName = 'redis_{$port}'

	downloadUrl = 'http://download.redis.io/redis-stable.tar.gz'
	defaultPort = '6379'

	paths = {
		'archPath': '/tmp/redis-stable/',
		'archInitDPath': '{$archPath}utils/redis_init_script',
		'archConfPath': '{$archPath}redis.conf',
		'etcFolder': '/etc/redis/',
		'varFolder': '/var/redis/',
		'initDPath': '/etc/init.d/{$serviceName}',
		'confPath': '{$etcFolder}{$port}.conf',
		'deletePath': '/usr/local/bin/redis*'
	}
	confChanges = {
		'daemonize no': 'daemonize yes',
		'pidfile /var/run/redis.pid': 'pidfile /var/run/{$serviceName}.pid',
		'logfile ""': 'logfile /var/log/{$serviceName}.log',
		'dir ./': 'dir {$varFolder}{$port}'
	}
	initDConf = {
		'REDISPORT=6379': 'REDISPORT={$port}'
	}

	def installDebian(self):
		port = self.attrs['port'] if 'port' in self.attrs else self.defaultPort
		self.init()

		self.wgetUnpack(self.downloadUrl)
		self.makeInstall(self.paths['archPath'])

		self.mkdir([self.paths['etcFolder'], self.paths['varFolder'] + port])
		self.cp(self.paths['archInitDPath'], self.paths['initDPath'])
		self.editFile(self.paths['initDPath'], self.initDConf)
		self.cp(self.paths['archConfPath'], self.paths['confPath'])
		self.editFile(self.paths['confPath'], self.confChanges)

		self.currentDist.updateInitScript(self.serviceName)
		self.currentDist.servStart(self.serviceName)
		self.rm(self.paths['archPath'])

	def delete(self):
		self.init()
		self.rm([self.paths['etcFolder'], self.paths['varFolder'], self.paths['initDPath'], self.paths['deletePath']])
		self.currentDist.removeInitScript(self.serviceName)

	def init(self):
		port = self.attrs['port'] if 'port' in self.attrs else self.defaultPort
		self.serviceName = self.serviceName.replace('{$port}', port)
		self.setPaths({'port': port, 'serviceName': self.serviceName})
		self.setPaths({'port': port, 'varFolder': self.paths['varFolder'], 'serviceName': self.serviceName}, self.confChanges)
		self.setPaths({'port': port}, self.initDConf)		
