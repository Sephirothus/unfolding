from Helper import Helper
from dists.Ubuntu import Ubuntu

class Nodejs:

	name = 'Node.js'

	def installUbuntu(self):
		myDist = Ubuntu()
		print myDist.aptGet('nodejs')

	def check(self):
		return (Helper()).checkVersion('nodejs')