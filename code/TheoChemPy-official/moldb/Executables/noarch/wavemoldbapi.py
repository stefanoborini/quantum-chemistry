import httplib, mimetypes
import urlparse
import simplejson
import logging

def posturl(url, fields, files, headers=None):
    urlparts = urlparse.urlsplit(url)
    return post_multipart(urlparts[1], urlparts[2], fields,files, headers)

def post_multipart(host, selector, fields, files, headers=None):
    content_type, body = encode_multipart_formdata(fields, files)
    logging.debug("Connecting to "+host+selector)
    h = httplib.HTTPConnection(host)
    if headers is None:
        headers = {
        'User-Agent': 'grrm2moldb',
        'Content-Type': content_type
        }
    if not headers.has_key("Content-Type"):
        headers["Content-Type"] = content_type

    h.request('POST', selector, body, headers)
    res = h.getresponse()
    return res.status, res.reason, res.read()



def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


class Wavemoldb(object):
    def __init__(self, base_url):
        self._base_url = base_url 

    def create_run(self, type_uri):
        jsondata = simplejson.dumps({ "type_uri": type_uri} )
        status, message, payload = posturl(self._base_url+"/api/v1/runs", [ ("json", jsondata) ], [] )
        if status == 201:
            data = simplejson.loads(payload)
            return data["uuid"]
        else:
            return None

    def create_collection(self, content):
        jsondata = simplejson.dumps({ "content" : content })
        status, message, payload = posturl(self._base_url+"/api/v1/collections", [ ("json", jsondata) ], [] )
        if status == 201:
            data = simplejson.loads(payload)
            return data["uuid"]
        else:
            return None

    def update_molecule(self, molecule_id):
        data = { }

        data["uuid"] = molecule_id
        jsondata = simplejson.dumps(data)
        status, message, payload = posturl(self._base_url+"/api/v1/molecules/%7B"+molecule_id+"%7D", [ ("json", jsondata) ], [], { "X-HTTP-Method-Override" : "PUT" } )

    def set_run_input(self, run_id, input_id):
        self.insert_triple( "urn:uuid:"+run_id, "http://ontologies.wavemol.org/moldb/v1/#Run_Input", "urn:uuid:"+input_id)

    def set_run_output(self, run_id, output_id):
        self.insert_triple( "urn:uuid:"+run_id, "http://ontologies.wavemol.org/moldb/v1/#Run_Output", "urn:uuid:"+output_id)

    def add_molecule_to_collection(self, collection_id, molecule_id):
        self.insert_triple( "urn:uuid:"+run_id, "http://ontologies.wavemol.org/moldb/v1/#Folder_Run_Input", "urn:uuid:"+input_id)

    def insert_triples(self, triple_list):
        for s,p,o in triple_list:
            insert_triple(s,p,o)

    def insert_triple(self, subject, predicate, object):
        data = (subject,predicate,object) 

        jsondata = simplejson.dumps(data)
        status, message, payload = posturl(self._base_url+"/api/v1/triples", [ ("json", jsondata) ], [] )
