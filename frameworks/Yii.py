class Yii:

    dependencies = ['languages.Php', 'managers.Composer']

    def install(self, myDist):
        print "==================\nInstalling Yii 2.0 \n"
        myDist.execute('composer global require "fxp/composer-asset-plugin:~1.0.3"')
        myDist.execute('composer create-project --prefer-dist yiisoft/yii2-app-advanced yii-application')
        print "=================="
        