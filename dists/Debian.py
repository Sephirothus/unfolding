# -*- coding: utf-8 -*-

import re
from Helper import Helper

class Debian(Helper):

	def install(self, package, rep = False, key = False, chosenVersion = False):
		if rep:
			# adding key if exists
			if key:
				# if key is url, we download it
				checkForUrl = re.search('^http[s]?:\/\/\S+', key)
				if checkForUrl:
					key = self.wget(key, '/tmp')
					method = 'add'
				else:
					method = 'adv'
				self.execute('sudo apt-key ' + method + ' ' + key)
				if checkForUrl: self.rm(key)
			# add repository
			self.execute('sudo add-apt-repository --yes "' + rep + '"')
			self.aptGetUpdate()
			# if isset concrete version, add full name of it
			if chosenVersion:
				versTable = self.aptCachePolicy(package)
				package += '=' + re.search('Version\stable.+(' + re.escape(chosenVersion) + '\S+)', versTable, flags=re.DOTALL).group(0)

		return self.execute('sudo apt-get install --yes --force-yes ' + package)

	def delete(self, package, rep = False):
		if rep:
			self.execute('sudo add-apt-repository --remove --yes "' + rep + '"')
			self.aptGetUpdate()
		return self.execute('sudo apt-get purge --auto-remove --yes ' + package)

	def checkAptGet(self, package):
		installed = self.execute('apt-cache policy ' + package)
		return installed and 'Установлен: (отсутствует)' not in installed and 'Installed: (none)' not in installed

	def aptGetUpdate(self):
		self.execute('sudo apt-get update')

	def aptCachePolicy(self, package):
		self.execute('apt-cache policy ' + package)

	def getCandidateVersion(self, package):
		return re.search('Candidate:\s(\S+)', self.aptCachePolicy(package)).group(0)

	def servCom(self, service, command):
		return self.execute('sudo service ' + service + ' ' + command)

	def servStatus(self, service):
		return self.servCom(service, 'status')

	def servStop(self, service):
		return self.servCom(service, 'stop')

	def servStart(self, service):
		return self.servCom(service, 'start')

	def getRelease(self, path = False):
		lsbRelease = self.execute('lsb_release -sc').strip()
		if path: 
			lsbRelease = path.replace('{$lsb_release}', lsbRelease)
		return lsbRelease

	def wgetAddpkg(self, filePath):
		filePath = self.wget(filePath, '/tmp')
		self.execute('dpkg -i ' + filePath)
		self.rm(filePath)
		self.aptGetUpdate()