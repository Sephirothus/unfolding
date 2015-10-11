class Nginx:

    dependencies = ['languages.Php']

    def install(self, myDist):
    	myDist.createBlock("Installing Nginx")
        myDist.aptGet('nginx')
        