# -*- coding: utf-8 -*-

import re
from Helper import Helper

class Ubuntu(Helper):

	def aptGet(self, package, rep = False, key = False, chosenVersion = False):
		if rep:
			# adding key if exists
			if key: self.execute('sudo apt-key add ' + key)
			# add repository
			self.execute('sudo add-apt-repository --yes "' + rep + '"')
			self.aptGetUpdate()
			# if isset concrete version, add full name of it
			if chosenVersion:
				versTable = self.aptCachePolicy(package)
				package += '=' + re.search('Version\stable.+(' + re.escape(chosenVersion) + '\S+)', versTable, flags=re.DOTALL).group(0)

		return self.execute('sudo apt-get install --yes --force-yes ' + package)

	def checkAptGet(self, package):
		installed = self.execute('apt-cache policy ' + package)
		return installed and 'Установлен: (отсутствует)' not in installed and 'Installed: (none)' not in installed

	def removeAptGet(self, package, rep = False):
		if rep:
			self.execute('sudo add-apt-repository --remove --yes "' + rep + '"')
			self.aptGetUpdate()
		return self.execute('sudo apt-get purge --auto-remove --yes ' + package)

	def aptGetUpdate(self):
		self.execute('sudo apt-get update')

	def aptCachePolicy(self, package):
		self.execute('apt-cache policy ' + package)

	def getCandidateVersion(self, package):
		return re.search('Candidate:\s(\S+)', self.aptCachePolicy(package)).group(0)

	def servStatus(self, service):
		return self.execute('sudo service ' + service + ' status')
