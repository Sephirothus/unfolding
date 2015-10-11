import subprocess

class Helper:

    def execute(self, command):
        return subprocess.Popen((command).split(), stdout=subprocess.PIPE).stdout.read()
    
    def getClass(self, moduleName):
        className = moduleName.rsplit(".", 1)[1]
        moduleName = __import__(moduleName, fromlist=[className]);
        return getattr(moduleName, className)

    def objAdd(self, val, data):
        for i in data:
            if i.__class__.__name__ == val.__class__.__name__:
                return False    
        data.append(val)

    def ucfirst(self, string):
        return string[0].upper() + string[1:]

    def getDist(self, conf):
        distName = ''
        if 'dists' in conf:
            distName = conf['dists']
        else:
            grep = self.execute("cat /etc/lsb-release")
            distName = grep.split('\n')[0].split('=')[1].lower()

        return self.getClass('dists.' + self.ucfirst(distName))()

    def createBlock(self, data):
        maxLen = len(max(data)) if type(data) is list else len(data)
        print "\n" + ("=" * (maxLen+4))

        if type(data) is list:
            for el in data:
                curLen = len(el)
                print "| " + el + (" " * (maxLen - curLen)) + " |"
        else:
            print "| " + data + " |"

        print "=" * (maxLen+4)

    def editFile(self, fileName, changes):
        fileData = open(fileName, "r")
        newData = fileData.read()
        for oldVal, newVal in changes.iteritems():
            newData = newData.replace(oldVal, newVal)
        fileData.close()

        fileData = open(fileName, "w")
        fileData.write(newData)
        fileData.close()
        