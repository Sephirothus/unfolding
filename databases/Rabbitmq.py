from dists.Ubuntu import Ubuntu

class Rabbitmq:

	name = 'RabbitMQ'
	serviceName = 'rabbitmq-server'
	repository = "deb http://www.rabbitmq.com/debian/ testing main"
	key = 'http://www.rabbitmq.com/rabbitmq-signing-key-public.asc'

	def installUbuntu(self):
		myDist = Ubuntu()
		key = myDist.wget(self.key, '/tmp')
		myDist.aptGet(self.serviceName, self.repository, key)
		myDist.rm(key)

	def checkUbuntu(self):
		return "Status of node" in (Ubuntu()).servStatus(self.serviceName)

	def deleteUbuntu(self):
		return (Ubuntu()).removeAptGet(self.serviceName, self.repository)