from Helper import Helper

class Nginx:

	name = 'Nginx'
	serviceName = 'nginx'
	logPath = '/var/log/nginx'
	pathAvailable = '/etc/nginx/sites-available/'
	pathEnabled = '/etc/nginx/sites-enabled/'

	def installUbuntu(self):
		self.curDist.aptGet(self.serviceName)

	def check(self):
		return (Helper()).checkVersion(self.serviceName, '-v')

	def deleteUbuntu(self):
		self.curDist.removeAptGet(self.serviceName)

	def restart(self):
		(Helper()).execute('sudo /etc/init.d/' + self.serviceName + ' restart')

	def enableSite(self, siteName):
		(Helper()).execute('sudo ln -s ' + self.pathAvailable + '/' + siteName + ' ' + self.pathEnabled)

	def disableSite(self, siteName):
		(Helper()).rm(self.pathEnabled + '/' + siteName)
		
	def siteConf(self, siteName, folder):
		return "\
server {\
    listen *:8080;\
    server_name " + siteName + ";\
    root " + folder + ";\
    index index.php index.html index.htm;\
\
    location / {\
    	limit_req zone=one burst=15\
        try_files $uri $uri/ @handler;\
    }\
\
    location ~* \.(png|jpeg|jpg|gif|ico)$ {\
		expires 1y;\
		log_not_found off;\
    }\
\
    location @handler {\
    	rewrite / /index.php;\
    }\
\
    error_log " + self.logPath + "/error." + siteName + ".log;\
    access_log " + self.logPath + "/access." + siteName + ".log;\
\
    location ~ \.php$ {\
        try_files $uri =404;\
        fastcgi_split_path_info ^(.+\.php)(/.+)$;\
        fastcgi_pass unix:/var/run/php5-fpm.sock;\
        fastcgi_index index.php;\
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;\
        include fastcgi_params;\
        rewrite ^(.*\.php)/ $1 last;\
    }\
}"
		