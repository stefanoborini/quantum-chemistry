# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../.."));
import unittest

from TheoChemPy.Net import SSHNode

def moduleDir():
    return os.path.dirname(__file__)

class MockTransport:
    def connect(self, hostkey=None, username='', password=None, pkey=None):
        print "connect "
    
    def __init__(self,t):
        host , port = t
        print host, port

    def close(self):
        pass
class MockSFTPClient:
    def put(self, source, dest):
        pass
    def get(self, source, dest):
        pass
    @classmethod
    def from_transport(cls,transport):
        print "from transport"
        return cls()
    def close(self):
        pass

class MockRSAKey:
    @classmethod
    def from_private_key_file(cls, filename, password=None):
        return cls()

class MockDSSKey:
    @classmethod
    def from_private_key_file(cls, filename, password=None):
        return cls()

def _mockGetTransportClass():
    return MockTransport

def _mockGetSFTPClientClass():
    return MockSFTPClient

def _mockGetRSAKeyClass():
    return MockRSAKey

def _mockGetDSSKeyClass():
    return MockDSSKey

SSHNode._getTransportClass=_mockGetTransportClass
SSHNode._getSFTPClientClass=_mockGetSFTPClientClass
SSHNode._getRSAKeyClass=_mockGetRSAKeyClass
SSHNode._getDSSKeyClass=_mockGetDSSKeyClass

class TestSSHNode(unittest.TestCase):
    def testInit(self): # fold>>
        
        host = "foo.bar"
        username = "luser"
        password = "word"
        private_key = "/path/to/key"
        port = 666

        node = SSHNode.SSHNode( host, username=username, password=password, private_key=private_key, port=port)

        self.assertEqual(node._host, "foo.bar")
        self.assertEqual(node._username, "luser")
        self.assertEqual(node._password, "word")
        self.assertEqual(node._private_key, "/path/to/key")
        self.assertEqual(node._port, 666)
        # <<fold
    def testInit2(self): # fold>>
        
        host = "foo.bar"
        password = "word"

        node = SSHNode.SSHNode( host, password=password)

        self.assertEqual(node._host, "foo.bar")
        self.assertNotEqual(node._username, None)
        self.assertEqual(node._password, "word")
        self.assertEqual(node._private_key, None)
        self.assertEqual(node._port, 22)
        # <<fold
    def testGet(self): # fold>>
        
        host = "foo.bar"
        username = "luser"
        password = "word"
        private_key = "/path/to/key"
        port = 666

        node = SSHNode.SSHNode( host, username=username, password=password, private_key=private_key, port=port)
        node.get("filein", "fileout")
        
        # <<fold
    def testPut(self): # fold>>
        
        host = "foo.bar"
        username = "luser"
        password = "word"
        private_key = "/path/to/key"
        port = 666

        node = SSHNode.SSHNode( host, username=username, password=password, private_key=private_key, port=port)
        node.put("filein", "fileout")
        
        # <<fold


if __name__ == '__main__':
    unittest.main()
    
