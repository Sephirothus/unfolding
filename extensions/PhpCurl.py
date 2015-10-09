class PhpCurl:

    dependencies = ['languages.Php']
    
    def install(self, myDist):
        myDist.createBlock("Installing curl libcurl3 libcurl3-dev php5-curl")
        myDist.aptGet('curl libcurl3 libcurl3-dev php5-curl')
