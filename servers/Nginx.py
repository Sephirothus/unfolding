from dists.Ubuntu import Ubuntu

class Nginx:

	name = 'Nginx'

	def installUbuntu(self):
		myDist = Ubuntu()
		print myDist.aptGet('nginx')
		