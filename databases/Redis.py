class Redis:

	name = 'Redis'

	def installUbuntu(self):
		port = self.attrs['port'] if hasattr(self, 'attrs') and 'port' in self.attrs else '6379'
		archPath = '/tmp/redis-stable/'

		self.curDist.wgetUnpack('http://download.redis.io/redis-stable.tar.gz')
		self.curDist.execute('sudo make -C ' + archPath)
		self.curDist.execute('sudo make install -C ' + archPath)

		self.curDist.execute('sudo mkdir /etc/redis')
		self.curDist.execute('sudo mkdir /var/redis')
		self.curDist.execute('sudo cp ' + archPath + 'utils/redis_init_script /etc/init.d/redis_' + port)

		self.curDist.editFile('/etc/init.d/redis_6379', {'REDISPORT=6379': 'REDISPORT=' + port})

		self.curDist.execute('sudo cp ' + archPath + 'redis.conf /etc/redis/' + port + '.conf')
		self.curDist.execute('sudo mkdir /var/redis/' + port)

		self.curDist.editFile('/etc/redis/' + port + '.conf', {
			'daemonize no': 'daemonize yes',
			'pidfile /var/run/redis.pid': 'pidfile /var/run/redis_' + port + '.pid',
			'logfile ""': 'logfile /var/log/redis_' + port + '.log',
			'dir ./': 'dir /var/redis/' + port
		})

		self.curDist.execute('sudo update-rc.d redis_' + port + ' defaults')
		self.curDist.execute('sudo service redis_' + port + ' start')
		self.curDist.execute('sudo rm -rf ' + archPath)