# -*- coding: utf-8 -*-

from Helper import Helper

class Ubuntu(Helper):

	def aptGet(self, name, rep=False):
		if rep:
			self.execute('sudo add-apt-repository ' + rep)
			self.execute('sudo apt-get update')

		return self.execute('sudo apt-get install --yes --force-yes ' + name)

	def checkAptGet(self, package):
		installed = self.execute('apt-cache policy ' + package)
		return installed and 'Установлен: (отсутствует)' not in installed and 'Installed: (none)' not in installed

	def removeAptGet(self, package):
		return self.execute('sudo apt-get purge --auto-remove ' + package)

	def wgetUntar(self, filePath):
		fileName = filePath.rsplit('/', 1)[1]
		self.execute('wget -P /tmp ' + filePath)
		self.execute('tar xvzf /tmp/' + fileName + ' -C /tmp')
		self.execute('rm /tmp/' + fileName)

	def install(self):
		return False

	def servStatus(self, service):
		return self.execute('sudo service ' + service + ' status')

	
