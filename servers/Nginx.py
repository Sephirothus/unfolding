from dists.Ubuntu import Ubuntu
from Helper import Helper

class Nginx:

	name = 'Nginx'

	def installUbuntu(self):
		myDist = Ubuntu()
		print myDist.aptGet('nginx')

	def check(self):
		return (Helper()).checkVersion('nginx')

	def deleteUbuntu(self):
		return (Ubuntu()).removeAptGet('nginx')

	def restart(self):
		(Helper()).execute('sudo service nginx restart')

	def addSite(self, siteName, folder):
		return False
		
	def siteConf(self, siteName, folder):
		return ''
		