from Helper import Helper
from dists.RouterDist import RouterDist

class Nodejs(RouterDist):

	name = 'Node.js'

	checkName = 'nodejs'
	packages = {
		'Debian': {
			'serviceName': 'nodejs'
		}
	}
