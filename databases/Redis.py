from dists.Ubuntu import Ubuntu

class Redis:

	name = 'Redis'

	def installUbuntu(self):
		myDist = Ubuntu()
		port = self.attrs['port'] if hasattr(self, 'attrs') and 'port' in self.attrs else '6379'
		archPath = '/tmp/redis-stable/'

		myDist.wgetUntar('http://download.redis.io/redis-stable.tar.gz')
		myDist.execute('sudo make -C ' + archPath)
		myDist.execute('sudo make install -C ' + archPath)

		myDist.execute('sudo mkdir /etc/redis')
		myDist.execute('sudo mkdir /var/redis')
		myDist.execute('sudo cp ' + archPath + 'utils/redis_init_script /etc/init.d/redis_' + port)

		myDist.editFile('/etc/init.d/redis_6379', {'REDISPORT=6379': 'REDISPORT=' + port})

		myDist.execute('sudo cp ' + archPath + 'redis.conf /etc/redis/' + port + '.conf')
		myDist.execute('sudo mkdir /var/redis/' + port)

		myDist.editFile('/etc/redis/' + port + '.conf', {
			'daemonize no': 'daemonize yes',
			'pidfile /var/run/redis.pid': 'pidfile /var/run/redis_' + port + '.pid',
			'logfile ""': 'logfile /var/log/redis_' + port + '.log',
			'dir ./': 'dir /var/redis/' + port
		})

		myDist.execute('sudo update-rc.d redis_' + port + ' defaults')
		myDist.execute('sudo service redis_' + port + ' start')
		myDist.execute('sudo rm -rf ' + archPath)