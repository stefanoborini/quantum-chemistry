# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../.."));
import unittest

from theochempy._theochempy.Net import SSHNode

def moduleDir():
    return os.path.dirname(__file__)

# contains a dictionary which keeps track of the number of calls each method
# receives. Each tests resets this dictionary holder to an empty dict, and at the 
# end of the test, the expected values are checked

class Counter:
    _counter = None

    @classmethod
    def _inc_counter(cls, symbol):
        if cls._counter.has_key(symbol):
            cls._counter[symbol] += cls._counter[symbol]
        else:
            cls._counter[symbol] = 1
    @classmethod
    def _init_counter(cls):
        cls._counter = {}

class MockTransport:
    def __init__(self,t): 
        Counter._inc_counter(self.__class__.__name__+"."+sys._getframe().f_code.co_name)
    def connect(self, hostkey=None, username='', password=None, pkey=None): 
        Counter._inc_counter(self.__class__.__name__+"."+sys._getframe().f_code.co_name)
    def close(self):
        Counter._inc_counter(self.__class__.__name__+"."+sys._getframe().f_code.co_name)
    def open_session(self):
        Counter._inc_counter(self.__class__.__name__+"."+sys._getframe().f_code.co_name)
        return MockChannel()

class MockSFTPClient:
    def put(self, source, dest):
        Counter._inc_counter(self.__class__.__name__+"."+sys._getframe().f_code.co_name)
    def get(self, source, dest):
        Counter._inc_counter(self.__class__.__name__+"."+sys._getframe().f_code.co_name)
    @classmethod
    def from_transport(cls,transport):
        Counter._inc_counter(cls.__name__+"."+sys._getframe().f_code.co_name)
        return cls()
    def close(self):
        Counter._inc_counter(self.__class__.__name__+"."+sys._getframe().f_code.co_name)

class MockRSAKey:
    @classmethod
    def from_private_key_file(cls, filename, password=None):
        Counter._inc_counter(cls.__name__+"."+sys._getframe().f_code.co_name)
        return cls()

class MockDSSKey:
    @classmethod
    def from_private_key_file(cls, filename, password=None):
        Counter._inc_counter(cls.__name__+"."+sys._getframe().f_code.co_name)
        return cls()

class MockChannel:
    def exec_command(self, command):
        Counter._inc_counter(self.__class__.__name__+"."+sys._getframe().f_code.co_name)

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
        Counter._init_counter()
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
        
        self.assertEqual(len(Counter._counter.keys()), 0)

        # <<fold
    def testInit2(self): # fold>>
        Counter._init_counter()
        
        host = "foo.bar"
        password = "word"

        node = SSHNode.SSHNode( host, password=password)

        self.assertEqual(node._host, "foo.bar")
        self.assertNotEqual(node._username, None)
        self.assertEqual(node._password, "word")
        self.assertEqual(node._private_key, None)
        self.assertEqual(node._port, 22)
        self.assertEqual(len(Counter._counter.keys()), 0)
        # <<fold
    def testGet(self): # fold>>
        Counter._init_counter()
        
        host = "foo.bar"
        username = "luser"
        password = "word"
        private_key = "/path/to/key"
        port = 666

        node = SSHNode.SSHNode( host, username=username, password=password, private_key=private_key, port=port)
        node.get("filein", "fileout")

        self.assertEqual(Counter._counter["MockTransport.__init__"], 1)
        self.assertEqual(Counter._counter["MockTransport.connect"], 1)
        self.assertEqual(Counter._counter.has_key("MockRSAKey.from_private_key_file"), False)
        self.assertEqual(Counter._counter.has_key("MockDSSKey.from_private_key_file"), False)
        self.assertEqual(Counter._counter["MockSFTPClient.from_transport"],1)
        self.assertEqual(Counter._counter["MockSFTPClient.get"],1)
        self.assertEqual(Counter._counter["MockSFTPClient.close"],1)
        self.assertEqual(Counter._counter["MockTransport.close"],1)

        # <<fold
    def testPut(self): # fold>>
        Counter._init_counter()
        
        host = "foo.bar"
        username = "luser"
        password = "word"
        private_key = "/path/to/key"
        port = 666

        node = SSHNode.SSHNode( host, username=username, password=password, private_key=private_key, port=port)
        node.put("filein", "fileout")
        
        self.assertEqual(Counter._counter["MockTransport.__init__"], 1)
        self.assertEqual(Counter._counter["MockTransport.connect"], 1)
        self.assertEqual(Counter._counter.has_key("MockRSAKey.from_private_key_file"), False)
        self.assertEqual(Counter._counter.has_key("MockDSSKey.from_private_key_file"), False)
        self.assertEqual(Counter._counter["MockSFTPClient.from_transport"],1)
        self.assertEqual(Counter._counter["MockSFTPClient.put"],1)
        self.assertEqual(Counter._counter["MockSFTPClient.close"],1)
        self.assertEqual(Counter._counter["MockTransport.close"],1)
        
        # <<fold
    def testExecute(self): # fold>>
        Counter._init_counter()
        
        host = "foo.bar"
        username = "luser"
        password = "word"
        private_key = "/path/to/key"
        port = 666

        node = SSHNode.SSHNode( host, username=username, password=password, private_key=private_key, port=port)
        node.execute("ls")

        self.assertEqual(Counter._counter["MockTransport.__init__"], 1)
        self.assertEqual(Counter._counter["MockTransport.open_session"], 1)
        self.assertEqual(Counter._counter["MockChannel.exec_command"],1)
        self.assertEqual(Counter._counter["MockTransport.close"], 1)
        
        # <<fold


if __name__ == '__main__':
    unittest.main()
    
