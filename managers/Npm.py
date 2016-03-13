from Helper import Helper
from dists.Ubuntu import Ubuntu

class Npm:

	name = 'npm'

	def installUbuntu(self):
		print (Ubuntu()).aptGet('npm')

	def check(self):
		return (Helper()).checkVersion('npm')

	def deleteUbuntu(self):
		return (Ubuntu()).removeAptGet('npm')
