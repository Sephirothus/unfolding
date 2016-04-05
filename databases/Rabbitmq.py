from dists.RouterDist import RouterDist

class Rabbitmq(RouterDist):

	name = 'RabbitMQ'
	serviceName = 'rabbitmq-server'
	repository = "deb http://www.rabbitmq.com/debian/ testing main"
	key = 'http://www.rabbitmq.com/rabbitmq-signing-key-public.asc'

	def installUbuntu(self):
		key = self.currentDist.wget(self.key, '/tmp')
		self.currentDist.aptGet(self.serviceName, self.repository, key)
		self.currentDist.rm(key)

	def checkUbuntu(self):
		return "Status of node" in self.currentDist.servStatus(self.serviceName)

	def deleteUbuntu(self):
		self.currentDist.removeAptGet(self.serviceName, self.repository)