from Helper import Helper
from dists.RouterDist import RouterDist

class Sphinx(RouterDist):

	name = "Sphinx"

	checkName = 'searchd'
	packages = {
		'Debian': {
			'serviceName': 'sphinxsearch'
		}
	}

	def configure(self):
		# add config file
		return False
