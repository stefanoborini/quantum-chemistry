# @author Stefano Borini
import os; import sys; sys.path.insert(1,os.path.realpath( os.path.join( os.path.dirname(__file__),"..") ) )
from lib import filestorage
import unittest
import shutil
class TestFileStorage(unittest.TestCase):
    def testInitLocal(self):
        shutil.rmtree(os.path.join(os.path.dirname(__file__),"local","foo"))
        settings = { "WEB_CACHE_BASE_DIR" : os.path.join(os.path.dirname(__file__),"web"),
                     "LOCAL_CACHE_BASE_DIR" : os.path.join(os.path.dirname(__file__),"local"),
                     "WEB_CACHE_WEB_BASE_URL" : "/foo",
                    }
        f=filestorage.FileStorage("foo", False, settings)
        self.assertNotEqual(f, None)
        self.assertEqual(os.path.exists(os.path.join(os.path.dirname(__file__),"local","foo")), True)

    def testInitWeb(self):
        shutil.rmtree(os.path.join(os.path.dirname(__file__),"web","foo"))
        settings = { "WEB_CACHE_BASE_DIR" : os.path.join(os.path.dirname(__file__),"web"),
                     "LOCAL_CACHE_BASE_DIR" : os.path.join(os.path.dirname(__file__),"local"),
                     "WEB_CACHE_WEB_BASE_URL" : "/foox",
                    }
        f=filestorage.FileStorage("foo", True, settings)
        self.assertNotEqual(f, None)
        self.assertEqual(os.path.exists(os.path.join(os.path.dirname(__file__),"web","foo")), True)
        self.assertEqual(f.url("bar"),"/foox/foo/bar")

    def testExists(self):
        shutil.rmtree(os.path.join(os.path.dirname(__file__),"web","foo"))
        settings = { "WEB_CACHE_BASE_DIR" : os.path.join(os.path.dirname(__file__),"web"),
                     "LOCAL_CACHE_BASE_DIR" : os.path.join(os.path.dirname(__file__),"local"),
                     "WEB_CACHE_WEB_BASE_URL" : "/foox",
                    }
        f=filestorage.FileStorage("foo", True, settings)
        self.assertEqual(f.exists("bar"), False)

    def testReadable(self):
        shutil.rmtree(os.path.join(os.path.dirname(__file__),"web","foo"))
        settings = { "WEB_CACHE_BASE_DIR" : os.path.join(os.path.dirname(__file__),"web"),
                     "LOCAL_CACHE_BASE_DIR" : os.path.join(os.path.dirname(__file__),"local"),
                     "WEB_CACHE_WEB_BASE_URL" : "/foox",
                    }
        f=filestorage.FileStorage("foo", True, settings)
        self.assertEqual(f.readable("bar"), False)
        
if __name__ == '__main__':
    unittest.main()

