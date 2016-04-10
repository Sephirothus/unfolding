from dists.RouterDist import RouterDist

class Rabbitmq(RouterDist):

	name = 'RabbitMQ'

	packages = {
		'Debian': {
			'serviceName': 'rabbitmq-server',
			'repository': 'deb http://www.rabbitmq.com/debian/ testing main',
			'key': 'http://www.rabbitmq.com/rabbitmq-signing-key-public.asc'
		}
	}

	def checkDebian(self):
		return "Status of node" in self.currentDist.servStatus(self.packages['Debian']['serviceName'])
