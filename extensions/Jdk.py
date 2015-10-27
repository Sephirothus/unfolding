from dists.Ubuntu import Ubuntu

class Jdk:

	name = 'Jdk'
	
	def installUbuntu(self):
		print (Ubuntu()).aptGet('default-jdk')
