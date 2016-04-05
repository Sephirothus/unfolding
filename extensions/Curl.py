from dists.RouterDist import RouterDist

class Curl(RouterDist):

	name = 'curl libcurl3 libcurl3-dev'
	
	def installUbuntu(self):
		self.currentDist.aptGet(self.name)
