import os
import tempfile

try:
    import paramiko
except:
    print "Unable to import paramiko. Cannot use SSH support. Check your paramiko installation"
    raise

class SSHNode:
    def __init__(self, host, username=None, password=None, private_key=None, port=22,):
        if username is None:
            username = os.environ['LOGNAME']
        self._host = host
        self._username = username
        self._private_key = private_key
        self._password = password
        self._port = port

    def get(self, source, dest):

        transport = _getTransportClass()((self._host, self._port))

        if self._password is not None:
            transport.connect(username=self._username, password=self._password)
        else:
            if self._private_key is None:
                if os.path.exists(os.path.expanduser('~/.ssh/id_rsa')):
                    private_key_full_path = os.path.expanduser('~/.ssh/id_rsa')
                    pkey = _getRSAKeyClass().from_private_key_file(private_key_full_path)
                elif os.path.exists(os.path.expanduser('~/.ssh/id_dsa')):
                    private_key_full_path = os.path.expanduser('~/.ssh/id_dsa')
                    pkey = _getDSSKeyClass().from_private_key_file(private_key_full_path)
                else:
                    raise Exception("No authentication method found (tried password, private key)")
            transport.connect(username=self._username,pkey=pkey)

        sftpclient = _getSFTPClientClass().from_transport(transport)
        sftpclient.get(source, dest)
        sftpclient.close()
        transport.close()

    def put(self, source, dest):

        transport = _getTransportClass()((self._host, self._port))

        if self._password is not None:
            transport.connect(username=self._username, password=self._password)
        else:
            if self._private_key is None:
                if os.path.exists(os.path.expanduser('~/.ssh/id_rsa')):
                    private_key_full_path = os.path.expanduser('~/.ssh/id_rsa')
                    pkey = _getRSAKeyClass().from_private_key_file(private_key_full_path)
                elif os.path.exists(os.path.expanduser('~/.ssh/id_dsa')):
                    private_key_full_path = os.path.expanduser('~/.ssh/id_dsa')
                    pkey = _getDSSKeyClass().from_private_key_file(private_key_full_path)
                else:
                    raise Exception("No authentication method found (tried password, private key)")
            transport.connect(username=self._username,pkey=pkey)

        sftpclient = _getSFTPClientClass().from_transport(transport)
        sftpclient.put(source, dest)
        sftpclient.close()
        transport.close()
        
    def exec(self, command):
        transport = _getTransportClass()((self._host, self._port))
        session = transport.open_session()
        session.exec_command(command)


# for testability, this call will be replaced so to return a mock object
def _getSFTPClientClass():
    return paramiko.SFTPClient
def _getTransportClass():
    return paramiko.Transport
def _getRSAKeyClass():
    return paramiko.RSAKey
def _getDSSKeyClass():
    return paramiko.DSSKey
