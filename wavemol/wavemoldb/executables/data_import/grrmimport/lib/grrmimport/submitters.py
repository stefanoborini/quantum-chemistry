from . import httpcomm
from . import printout
import logging 

class FileSubmitter:
    def __init__(self, filename):
        self._filename = filename

    def submit(self, rdfxml):
        printout.info("Storing into file : "+str(self._filename))

        f=file(self._filename,"w")
        f.write(rdfxml)
        f.close()
        printout.info("Done")
            
class HttpSubmitter:
    def __init__(self, db_url):
        self._db_url = db_url
        
    def submit(self, rdfxml):
        printout.info("Submitting data to URL : "+str(self._db_url))

        status, message, payload = httpcomm.posturl(self._db_url+"/api/v2/import", [ ("xml", rdfxml) ], [] )
        printout.keyvalue("db_url",str(self._db_url))
        printout.keyvalue("status",str(status))
        printout.keyvalue("message",message)
        printout.keyvalue("payload",payload)
        printout.info("Done")

