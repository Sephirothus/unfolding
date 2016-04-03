from dists.RouterDist import RouterDist

class Rabbitmq(RouterDist):

	name = 'RabbitMQ'
	serviceName = 'rabbitmq-server'
	repository = "deb http://www.rabbitmq.com/debian/ testing main"
	key = 'http://www.rabbitmq.com/rabbitmq-signing-key-public.asc'

	def installUbuntu(self):
		key = self.dist.wget(self.key, '/tmp')
		self.dist.aptGet(self.serviceName, self.repository, key)
		self.dist.rm(key)

	def checkUbuntu(self):
		return "Status of node" in self.dist.servStatus(self.serviceName)

	def deleteUbuntu(self):
		self.dist.removeAptGet(self.serviceName, self.repository)