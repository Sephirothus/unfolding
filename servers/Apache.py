from dists.Ubuntu import Ubuntu

class Apache:

	name = "Apache"

	def installUbuntu(self):
		myDist = Ubuntu()
		print myDist.aptGet('apache2')

	def checkUbuntu(self):
		return "unrecognized service" not in (Ubuntu()).servStatus("apache2")