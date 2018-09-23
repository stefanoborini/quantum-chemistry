import shutil
import ssh

class LocalNode:
    def __init__(self):
        pass
    def putFile(self, source, dest):
        shutil.copytree(source, dest)
    def getFile(self, source, dest):
        shutil.copytree(source, dest)
    def execute(self, command):
        system(command)
