import sys
import json
import os.path

from Config import Config

# installs = {
# 	'apache2 | nginx',
# 	'php | python | ruby',
# 	'relational db (mysql | postgre)',
# 	'nosql db (redis | mongo)',
# 	'sphinx | elastic',
# 	'git | svn',
#	'dependencies managers - composer(for php)',
#	'build makers like gulp, Grunt',
# 	'framework'
# }
try:
	confClass = Config()
	conf = {}
	fileName = 'aa'#'my_config.json'

	if (os.path.isfile(fileName)):
		with open(fileName) as data_file:
			conf = json.load(data_file)

		conf['dist'] = Config.dist[conf['dist']]
	else:
		conf = confClass.makeConf()

	#cl = conf['dist']()
	# print cl.getConf()
	#print cl
	#print conf
	confClass.getClass(conf['dist'])(conf).install()
	
except KeyboardInterrupt:
	print "\nBye:)"
	