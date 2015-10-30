from Helper import Helper
from dists.Ubuntu import Ubuntu

class Npm:

	name = 'npm'

	def installUbuntu(self):
		myDist = Ubuntu()
		print myDist.aptGet('npm')

	def check(self):
		return (Helper()).checkVersion('npm')
