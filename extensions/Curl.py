class Curl:

	name = 'curl libcurl3 libcurl3-dev'
	
	def installUbuntu(self):
		self.curDist.aptGet(self.name)
