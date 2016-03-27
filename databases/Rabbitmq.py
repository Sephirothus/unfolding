class Rabbitmq:

	name = 'RabbitMQ'
	serviceName = 'rabbitmq-server'
	repository = "deb http://www.rabbitmq.com/debian/ testing main"
	key = 'http://www.rabbitmq.com/rabbitmq-signing-key-public.asc'

	def installUbuntu(self):
		key = self.curDist.wget(self.key, '/tmp')
		self.curDist.aptGet(self.serviceName, self.repository, key)
		self.curDist.rm(key)

	def checkUbuntu(self):
		return "Status of node" in self.curDist.servStatus(self.serviceName)

	def deleteUbuntu(self):
		self.curDist.removeAptGet(self.serviceName, self.repository)