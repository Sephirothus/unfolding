from dists.Ubuntu import Ubuntu
from Helper import Helper

class Sphinx:

	name = "Sphinx"
	
	def installUbuntu(self):
		myDist = Ubuntu()
		print myDist.aptGet('sphinxsearch')

	def deleteUbuntu(self):
		return (Ubuntu()).removeAptGet('sphinxsearch')

	def check(self):
		return (Helper()).checkVersion('searchd')
		