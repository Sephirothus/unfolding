from dists.RouterDist import RouterDist

class Redis(RouterDist):

	name = 'Redis'

	def installUbuntu(self):
		port = self.attrs['port'] if hasattr(self, 'attrs') and 'port' in self.attrs else '6379'
		archPath = '/tmp/redis-stable/'

		self.dist.wgetUnpack('http://download.redis.io/redis-stable.tar.gz')
		self.dist.execute('sudo make -C ' + archPath)
		self.dist.execute('sudo make install -C ' + archPath)

		self.dist.execute('sudo mkdir /etc/redis')
		self.dist.execute('sudo mkdir /var/redis')
		self.dist.execute('sudo cp ' + archPath + 'utils/redis_init_script /etc/init.d/redis_' + port)

		self.dist.editFile('/etc/init.d/redis_6379', {'REDISPORT=6379': 'REDISPORT=' + port})

		self.dist.execute('sudo cp ' + archPath + 'redis.conf /etc/redis/' + port + '.conf')
		self.dist.execute('sudo mkdir /var/redis/' + port)

		self.dist.editFile('/etc/redis/' + port + '.conf', {
			'daemonize no': 'daemonize yes',
			'pidfile /var/run/redis.pid': 'pidfile /var/run/redis_' + port + '.pid',
			'logfile ""': 'logfile /var/log/redis_' + port + '.log',
			'dir ./': 'dir /var/redis/' + port
		})

		self.dist.execute('sudo update-rc.d redis_' + port + ' defaults')
		self.dist.execute('sudo service redis_' + port + ' start')
		self.dist.execute('sudo rm -rf ' + archPath)