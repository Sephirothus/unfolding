from dists.RouterDist import RouterDist

class Curl(RouterDist):

	name = 'curl libcurl3 libcurl3-dev'

	packages = {
		'Debian': {
			'serviceName': 'curl libcurl3 libcurl3-dev'
		}
	}
