from dists.Ubuntu import Ubuntu
from Helper import Helper

class Nginx:

	name = 'Nginx'

	def installUbuntu(self):
		myDist = Ubuntu()
		print myDist.aptGet('nginx')

	def check(self):
		return (Helper()).checkVersion('nginx')

	def addSite(self, siteName, folder):
		return False
		
	def siteConf(self, siteName, folder):
		return ''
		