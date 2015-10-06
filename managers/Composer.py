class Composer:

    dependencies = ['languages.Php', 'extensions.PhpCurl']

    def install(self, myDist):
        print "==================\nInstalling Composer \n"
        myDist.execute('curl -sS https://getcomposer.org/installer | sudo php -- --install-dir=/usr/local/bin --filename=composer')
        print "=================="