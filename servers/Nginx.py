from dists.Ubuntu import Ubuntu

class Nginx:

	dependencies = ['languages.Php']
	name = 'Nginx'

	def installUbuntu(self):
		myDist = Ubuntu()
		myDist.aptGet('nginx')
		