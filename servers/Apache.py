from dists.Ubuntu import Ubuntu
from Helper import Helper

class Apache:

	name = "Apache"

	def installUbuntu(self):
		myDist = Ubuntu()
		print myDist.aptGet('apache2')

	def check(self):
		return (Helper()).checkVersion('apache2ctl')

	def addSite(self, siteName, folder):
		self.siteActions(siteName, self.siteConf(siteName, folder), '127.0.0.1   ' + siteName)

	def addSiteWithAliases(self, siteName, aliasesAndFolders):
		conf = ''
		host = ''
		for alias, folder in aliasesAndFolders.iteritems():
			site = alias + '.' + siteName if alias else siteName
			conf += self.siteConf(site, folder) + "\n\n"
			host += '127.0.0.1   ' + site + "\n"

		self.siteActions(siteName, conf, host)
			
	def siteActions(self, siteName, config, host):
		helper = Helper()
		path = '/etc/apache2/sites-available/' + siteName + '.conf'

		print "-- Save config file for server"
		helper.saveFile(path, config)
		print "-- Enabling site"
		helper.execute('sudo a2ensite ' + siteName)
		print "-- Restart service"
		helper.execute('sudo service apache2 restart')
		print "-- Add site to hosts"
		helper.addHost(host)

	def siteConf(self, siteName, folder):
		return "\
<VirtualHost 127.0.0.1:*>\n\
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
	ErrorLog ${APACHE_LOG_DIR}/error.log\n\
	CustomLog ${APACHE_LOG_DIR}/access.log combined\n\
</VirtualHost>"