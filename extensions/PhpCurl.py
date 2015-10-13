from dists.Ubuntu import Ubuntu

class PhpCurl:

	dependencies = ['languages.Php']
	name = 'curl libcurl3 libcurl3-dev php5-curl'
	
	def installUbuntu(self):
		myDist = Ubuntu()
		print myDist.aptGet('curl libcurl3 libcurl3-dev php5-curl')
