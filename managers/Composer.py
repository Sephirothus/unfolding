class Composer:

    dependencies = ['languages.Php', 'extensions.PhpCurl']

    def install(self, myDist):
        myDist.createBlock("Installing Composer")
        if self.check(myDist):
            print "Composer already installed"
        else:
            myDist.execute('sudo curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer')
            myDist.execute('sudo composer global require "fxp/composer-asset-plugin:~1.0.3"')
        
    def check(self, myDist):
        version = myDist.execute("composer --version")
        return "version" in version
