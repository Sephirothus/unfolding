from Helper import Helper
from dists.Ubuntu import Ubuntu

class Ruby:

	name = 'Ruby'
	
	def installUbuntu(self):
		myDist = Ubuntu()
		print myDist.aptGet('ruby-full')

	def check(self):
		return (Helper()).checkVersion('ruby')
