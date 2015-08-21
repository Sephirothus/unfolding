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

# args = {
# 	'install',
# 	'update'
# }
try:
	try:
		arg = sys.argv[1]
	except IndexError:
		arg = 'install'

	confClass = Config()
	conf = {}
	fileName = 'my_config.json'

	if (os.path.isfile(fileName)):
		with open(fileName) as data_file:
			conf = json.load(data_file)

		conf = confClass.makeConf(conf)
	else:
		conf = confClass.createConf()

	print conf
	#confClass.getClass(conf['dist'])(conf).install()
	
except KeyboardInterrupt:
	print "\nBye:)"
	