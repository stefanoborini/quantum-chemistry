import os
import cPickle
import fnmatch
import StringIO
import zipfile
import string


def init(path):
    if os.path.exists(path) and not os.path.isdir(path):
        raise Exception("path is not a dir")

    try:
        os.makedirs(os.path.join(path,".meta"))
    except:
        pass
    f = file(os.path.join(path,".meta", "version"), "w")
    f.write("1.0.0")
    f.close()

    f = file(os.path.join(path,".meta", "format"), "w")
    f.write("base")
    f.close()

class MyStringIO(StringIO.StringIO):
    """Wraps StringIO which unfortunately does not have __len__ method, meaning that it cannot be used in the pickling
    as it would be a file
    """ 
    def __len__(self):
        return self.len

class DBAccess:
    def __init__(self, path):
        if not os.path.exists(os.path.join(path, ".meta","version")):
            raise Exception("Not a database dir")
        if not os.path.exists(os.path.join(path, ".meta","format")):
            raise Exception("Not a database dir")
        self._path = path

    def store(self, graph):
        s = MyStringIO()
        f = zipfile.ZipFile(os.path.join(self._path, str(graph.uuid())+".gd"), "w")
        pickler = cPickle.Pickler(s)
        pickler.dump(graph)
        f.writestr("graph_data", s.getvalue())
        f.writestr("__graph_version", "1")
        f.close()


    def retrieveAll(self):
        all = []
        filenames = fnmatch.filter(os.listdir(self._path), "*.gd")
        for fname in filenames:
            try:
                f = zipfile.ZipFile(os.path.join(self._path, fname), "r")
                version = f.read("__graph_version")
            except IOError:
                continue

            if int(version) > 1:
                continue
            s = MyStringIO()
            s.write(f.read("graph_data"))
            s.seek(0)
            unpick = cPickle.Unpickler(s)
            graph = unpick.load()
            all.append(graph)
            f.close()
        return all
        
            
    def search(self, condition):
        results = []
        all = self.retrieveAll()
        for molecule in all:
            if condition.satisfiedBy(molecule):
                results.append(molecule)

        return results

    def metainfo(self,key):
        if not _isValidFilename(key):
            raise ValueError("Invalid key : %s" % key)

        try:
            f = file(os.path.join(self._path,".meta", key), "r")
            s = MyStringIO()
            s.write(f.read())
            s.seek(0)
            unpick = cPickle.Unpickler(s)
            value = unpick.load()
            f.close()
            return value
        except:
            return None




    def setMetainfo(self, key, value):
        if not _isValidFilename(key):
            raise ValueError("Invalid key : %s" % key)

        f = file(os.path.join(self._path,".meta", key), "w")
        s = MyStringIO()
        pickler = cPickle.Pickler(s)
        pickler.dump(value)
        f.write(s.getvalue())
        f.close()



def _isValidFilename(name):
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    mangled = ''.join(c for c in name if c in valid_chars)
    if mangled == name:
        return True
    return False

