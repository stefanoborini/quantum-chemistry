import subprocess
import tempfile
import os; import sys; sys.path.insert(1,os.path.realpath( os.path.join( os.path.dirname(__file__),"..","..",".." ) ) )
from lib import filestorage
from lib import uuid
from wavemoldb import ordfm
from wavemoldb.ordfm import grrm2
from wavemoldb.ordfm import contexts
import rdflib
import settings
from lib import chemistry
from rdflib.Graph import Graph

def _removeFile(path):
    try:
        os.rename(path, os.path.join(os.path.dirname(path), os.path.basename(path)+".REMOVE"))
    except:
        pass
def getSystemUuid(store, submission_uuid):
    graph = Graph(store, identifier=contexts.CONTEXT_NS.SubmissionInfo)
    submission = ordfm.OriginalSubmission.get(graph,uri="urn:uuid:"+submission_uuid)
    if submission is None:
        raise Exception("no submission found "+str(submission_uuid))
    storage = filestorage.ResourceStorage(submission, web_accessible=False, settings=settings.filestorage_settings)
    f=file(storage.path("system","uuid"), "r")
    id = str(uuid.UUID(f.readlines()[0]))
    f.close()
    return id

def generateFormula(mol):
    data = grrm2.geometry(mol).get()
    formula = chemistry.hillFormula(data["symbols"])
    return formula

def generateInchi(mol):
    fs= filestorage.ResourceStorage(mol, web_accessible=False, settings=settings.filestorage_settings)
    fs_web= filestorage.ResourceStorage(mol, web_accessible=True, settings=settings.filestorage_settings)

    xyz_path = fs_web.path("geometry","xyz")
    inchi_path = fs.path("inchi","txt")
    p = subprocess.Popen(["bwrap_xyz2inchi",xyz_path,inchi_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    retcode = p.wait()
    if retcode != 0:
        _removeFile(inchi_path)
        return None
    
    try:
        inchi_path = fs.path("inchi","txt") 
        f = file(inchi_path,"r")
        inchi = f.readlines()[0].strip()
        f.close()
    except:
        _removeFile(inchi_path)
        return None

    return inchi

def generateSmiles(mol):
    fs = filestorage.ResourceStorage(mol, web_accessible=False, settings=settings.filestorage_settings)
    fs_web= filestorage.ResourceStorage(mol, web_accessible=True, settings=settings.filestorage_settings)
    xyz_path = fs_web.path("geometry","xyz")
    smiles_path = fs.path("smiles","txt")
    p = subprocess.Popen(["bwrap_xyz2smiles",xyz_path,smiles_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    retcode = p.wait()
    if retcode != 0:
        _removeFile(smiles_path)
        return None
        
    try:
        smiles_path = fs.path("smiles","txt")
        f = file(smiles_path,"r")
        smiles = f.readlines()[0]
        f.close()
    except:
        _removeFile(smiles_path)
        return None

    return smiles

def generateMass(mol):
    fs = filestorage.ResourceStorage(mol, web_accessible=False, settings=settings.filestorage_settings)
    fs_web= filestorage.ResourceStorage(mol, web_accessible=True, settings=settings.filestorage_settings)
    xyz_path = fs_web.path("geometry","xyz")
    mass_path = fs.path("mass", "txt")
    p = subprocess.Popen(["bwrap_xyz2molweight",xyz_path,mass_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    retcode = p.wait()
    if retcode != 0:
        _removeFile(mass_path)
        return None
        
    try:
        mass_path = fs.path("mass", "txt")
        f = file(mass_path,"r")
        mass = float(f.readlines()[0])
        f.close()
    except:
        _removeFile(mass_path)
        return None

    return mass

def generateMdl(mol):
    fs = filestorage.ResourceStorage(mol, web_accessible=False, settings=settings.filestorage_settings)
    fs_web = filestorage.ResourceStorage(mol, web_accessible=True, settings=settings.filestorage_settings)
    xyz_path = fs_web.path("geometry","xyz")
    mol_path = fs.path("geometry", "mol")
    p = subprocess.Popen(["babel","-ixyz",xyz_path,"-omol",mol_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    retcode = p.wait()
    print "retcode mdl "+str(retcode)

    if retcode != 0:
        _removeFile(mol_path)
        raise Exception("Unable to create mdl")

def _generateCanostFromFile(molfile_path, canost_path, canost_type):
    if canost_type == "planar":
        option = "-ci"
    elif canost_type == "serial":
        option = "-ni"
    elif canost_type == "canonical":
        option = "-ui"

    p = subprocess.Popen(["cnrun","canost-2.9.2",option,"f", molfile_path,canost_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    retcode = p.wait()

    if retcode != 0:
        _removeFile(canost_path)
        return None

    try:
        f = file(canost_path,"r")
        canost = filter(lambda y: len(y) != 0, map(lambda x: x.strip(), f.readlines()))
        f.close()
    except:
        _removeFile(canost_path)
        return None

    if canost_type == "canonical":
        try:
            planar_canonical = canost[1]
            serial_canonical = canost[3]
        except:
            _removeFile(canost_path)
            return None
        
        if len(planar_canonical) == 0:
            planar_canonical = None
        if len(serial_canonical) == 0:
            serial_canonical = None
        canost = [planar_canonical, serial_canonical]
    
    if len(canost) == 0:
        _removeFile(canost_path)
        return None

    return canost

def generateCanostPlanar(mol):
    fs = filestorage.ResourceStorage(mol, web_accessible=False, settings=settings.filestorage_settings)
    fs_web= filestorage.ResourceStorage(mol, web_accessible=True, settings=settings.filestorage_settings)
    mol_path = fs.path("geometry","mol")
    canost_path = fs.path("canost_planar", "txt")
    return _generateCanostFromFile(mol_path, canost_path, "planar")

def generateCanostSerial(mol):
    fs = filestorage.ResourceStorage(mol, web_accessible=False, settings=settings.filestorage_settings)
    fs_web= filestorage.ResourceStorage(mol, web_accessible=True, settings=settings.filestorage_settings)
    mol_path = fs.path("geometry","mol")
    canost_path = fs.path("canost_serial", "txt")
    return _generateCanostFromFile(mol_path, canost_path, "serial")

def generateCanostCanonical(mol):
    fs = filestorage.ResourceStorage(mol, web_accessible=False, settings=settings.filestorage_settings)
    fs_web = filestorage.ResourceStorage(mol, web_accessible=True, settings=settings.filestorage_settings)
    mol_path = fs.path("geometry","mol")
    canost_path = fs.path("canost_canonical", "txt")

    return _generateCanostFromFile(mol_path, canost_path, "canonical")

def generateMdlForFragments(mol):
    fragments = grrm2.fragments(mol).get()
    print "Found fragments : "+str(fragments)
    if fragments:
        for fragment_number in xrange(len(fragments)):
            fs = filestorage.ResourceStorage(mol, web_accessible=False, settings=settings.filestorage_settings)
            fs_web= filestorage.ResourceStorage(mol, web_accessible=True, settings=settings.filestorage_settings)
            xyz_path = fs_web.path("geometry","xyz", parameters={"fragment" : fragment_number})
            mol_path = fs.path("geometry", "mol", parameters={ "fragment" : fragment_number})
            p = subprocess.Popen(["babel","-ixyz",xyz_path,"-omol",mol_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            print ["babel","-ixyz",xyz_path,"-omol",mol_path]
            retcode = p.wait()
            if retcode != 0:
                _removeFile(mol_path)
                raise Exception("Unable to create mdl for fragment "+str(fragment_number)+" molecule "+mol.uri())
    
    return None

def generateCanostPlanarFragments(mol):
    fragments = grrm2.fragments(mol).get()
    if not fragments:
        return None

    canost_planar_fragments = []
    for fragment_number in xrange(len(fragments)):
        fs = filestorage.ResourceStorage(mol, web_accessible=False, settings=settings.filestorage_settings)
        fs_web= filestorage.ResourceStorage(mol, web_accessible=True, settings=settings.filestorage_settings)
        mol_path = fs.path("geometry","mol", parameters={'fragment': fragment_number})
        canost_path = fs.path("canost_planar", "txt", parameters={"fragment": fragment_number})
        canost = _generateCanostFromFile(mol_path, canost_path, "planar")
        canost_planar_fragments.append(canost)

    return canost_planar_fragments

def generateCanostSerialFragments(mol):
    fragments = grrm2.fragments(mol).get()
    if not fragments:
        return None

    canost_serial_fragments = []
    for fragment_number in xrange(len(fragments)):
        fs = filestorage.ResourceStorage(mol, web_accessible=False, settings=settings.filestorage_settings)
        fs_web= filestorage.ResourceStorage(mol, web_accessible=True, settings=settings.filestorage_settings)
        mol_path = fs.path("geometry","mol", parameters={'fragment': fragment_number})
        canost_path = fs.path("canost_serial", "txt", parameters={"fragment": fragment_number})
        canost = _generateCanostFromFile(mol_path, canost_path, "serial")
        canost_serial_fragments.append(canost)

    return canost_serial_fragments

def generateCanostCanonicalFragments(mol):
    fragments = grrm2.fragments(mol).get()
    if not fragments:
        return None

    canost_canonical_fragments = []
    for fragment_number in xrange(len(fragments)):
        fs = filestorage.ResourceStorage(mol, web_accessible=False, settings=settings.filestorage_settings)
        fs_web = filestorage.ResourceStorage(mol, web_accessible=True, settings=settings.filestorage_settings)
        mol_path = fs.path("geometry","mol", parameters={"fragment": fragment_number})
        canost_path = fs.path("canost_canonical", "txt", parameters={"fragment":fragment_number})

        canost = _generateCanostFromFile(mol_path, canost_path, "canonical")

        canost_canonical_fragments.append(canost)

    return canost_canonical_fragments

