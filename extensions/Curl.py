from dists.Ubuntu import Ubuntu

class Curl:

	name = 'curl libcurl3 libcurl3-dev'
	
	def installUbuntu(self):
		(Ubuntu()).aptGet('curl libcurl3 libcurl3-dev')
