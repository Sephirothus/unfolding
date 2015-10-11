class Yii:

    dependencies = ['languages.Php', 'managers.Composer']

    def install(self, myDist):
        myDist.createBlock("Installing Yii 2.0")
        version = self.attrs['version'] if hasattr(self, 'attrs') and 'version' in self.attrs else 'basic'
        folder = self.attrs['folder'] if hasattr(self, 'attrs') and 'folder' in self.attrs else '../yii-application'

        myDist.composerProject('yiisoft/yii2-app-' + version + ' ' + folder)
        if version == 'advanced':
            myDist.execute('php ' + folder + '/init')
            
        # TODO db config, apache|nginx config, hosts