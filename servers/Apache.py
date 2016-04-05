from Helper import Helper
from dists.RouterDist import RouterDist

class Apache(RouterDist):

	name = "Apache"
	serviceName = 'apache2'
	path = '/etc/apache2/sites-available/'
	commandName = 'apache2ctl'

	def installUbuntu(self):
		self.currentDist.aptGet(self.serviceName)

	def check(self):
		return (Helper()).checkVersion(self.commandName)

	def deleteUbuntu(self):
		self.currentDist.removeAptGet(self.serviceName)

	def restart(self):
		(Helper()).execute('sudo /etc/init.d/' + self.serviceName + ' restart')

	def enableSite(self, siteName):
		(Helper()).execute('sudo a2ensite ' + siteName)

	def disableSite(self, siteName):
		(Helper()).execute('sudo a2dissite ' + siteName)

	def siteConf(self, siteName, folder):
		return "\
<VirtualHost *:80>\n\
	ServerName " + siteName + "\n\
	ServerAlias " + siteName + "\n\
	DocumentRoot " + folder + "\n\
\n\
	<Directory " + folder + ">\n\
		Options Indexes FollowSymLinks\n\
		AllowOverride All\n\
		Require all granted\n\
	</Directory>\n\
\n\
	ErrorLog ${APACHE_LOG_DIR}/error." + siteName + ".log\n\
	CustomLog ${APACHE_LOG_DIR}/access." + siteName + ".log combined\n\
</VirtualHost>"