class Rabbitmq:

	def install(self, myDist):
		myDist.createBlock("Installing RabbitMQ")
		
		myDist.execute('sudo echo "deb http://www.rabbitmq.com/debian/ testing main" >> /etc/apt/sources.list')
		myDist.execute('wget -P /tmp http://www.rabbitmq.com/rabbitmq-signing-key-public.asc')
		myDist.execute('sudo apt-key add /tmp/rabbitmq-signing-key-public.asc')
		myDist.execute('sudo apt-get update')
		myDist.aptGet('rabbitmq-server')
		myDist.execute('sudo rm /tmp/rabbitmq-signing-key-public.asc')
