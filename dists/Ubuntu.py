# -*- coding: utf-8 -*-

from Helper import Helper

class Ubuntu(Helper):

	def aptGet(self, name, rep=False):
		if rep:
			self.execute('sudo add-apt-repository ' + rep)
			self.aptGetUpdate()

		return self.execute('sudo apt-get install --yes --force-yes ' + name)

	def checkAptGet(self, package):
		installed = self.execute('apt-cache policy ' + package)
		return installed and 'Установлен: (отсутствует)' not in installed and 'Installed: (none)' not in installed

	def removeAptGet(self, package):
		return self.execute('sudo apt-get purge --auto-remove ' + package)

	def aptGetUpdate(self):
		self.execute('sudo apt-get update')

	def install(self):
		return False

	def servStatus(self, service):
		return self.execute('sudo service ' + service + ' status')

	
