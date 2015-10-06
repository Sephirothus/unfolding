class PhpCurl:

    dependencies = ['languages.Php']
    
    def install(self, myDist):
        print "==================\nInstalling curl libcurl3 libcurl3-dev php5-curl\n"
        myDist.aptGet('curl libcurl3 libcurl3-dev php5-curl')
        print "=================="
