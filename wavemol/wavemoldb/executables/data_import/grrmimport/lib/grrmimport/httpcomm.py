# from Wade Leftwich

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

