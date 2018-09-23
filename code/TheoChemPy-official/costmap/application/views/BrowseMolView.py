from django.shortcuts import render_to_response
from theochempy._theochempy.Databases.Simple import DBAccess
from theochempy._theochempy.GraphDataModel import InfosetType
from theochempy._theochempy import Units
from django.http import Http404
from django.utils import simplejson
import settings

import os


def browsemol(request, dbname, mol_code):
    try:
        db = DBAccess.DBAccess(os.path.join(settings.DB_PATH, dbname))
    except:
        raise Http404
    
    molecules = [x for x in db.retrieveAll()]

    mol = None
    for m in molecules:
        molecule_code_infoset = m.getInfosets(infoset_type=InfosetType.getMoleculeCodeType())
        if len(molecule_code_infoset) != 1:
            continue
        if molecule_code_infoset[0].value(None) == mol_code:
            mol = m
            break

    if mol is None:
        raise Http404
    
    infosets = mol.getInfosets()

    _createXYZFile(mol)
    infosets_data = []
    graph_infosets_data = []
    angle_data = []
    for i in infosets:
        if i.dimensionality() == 0:
            graph_infosets_data.append( (i.uuid(), i.value(None), i.typeURI()) )
        else:
            infosets_data.append( (i.uuid(), i.dimensionality(), i.typeURI(), i.size()) )
    return render_to_response("application/browsemol.html", { "dbname" : dbname, "molname" : str(mol.uuid()), "uuid" : str(mol.uuid()), "graph_infosets_data": graph_infosets_data, "infosets_data": infosets_data, "angle_data" : angle_data})

def _createXYZFile(mol):
    cache_dir = os.path.join(os.path.dirname(__file__),"..","..","cache","jmol")

    uuid = mol.uuid()
    element = mol.getInfosets(infoset_type=InfosetType.getElementType())[0]
    coords = mol.getInfosets(infoset_type=InfosetType.getCoordsType())[0]

    f = file(os.path.join(cache_dir,str(uuid)+".xyz"), "w")
    num_atoms = len(element.allValues())
    f.write(str(num_atoms)+"\n\n")
    for node, element in element.allValues():
        coordinates = coords.value(node).asUnit(Units.angstrom).value()
        f.write( "%s  %16.10f %16.10f %16.10f\n" % (element.symbol(), coordinates[0], coordinates[1], coordinates[2]) )

    f.close()

