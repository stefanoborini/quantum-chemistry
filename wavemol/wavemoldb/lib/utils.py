import uuid

def uriToUuid(uri):
    if uri[0:len("urn:uuid:")] != "urn:uuid:":
        raise ValueError("Invalid uri. not a urn:uuid:") 
    try:
        return str(uuid.UUID(uri.split(':')[2]))
    except:
        raise ValueError("Cannot convert uri to uuid : "+str(uri))

def uuidToUri(u_id):
    try:
        uuid.UUID(str(u_id))
    except:
        raise ValueError("Invalid uuid : "+str(u_id))
    return "urn:uuid:"+u_id

