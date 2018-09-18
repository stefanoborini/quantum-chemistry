from django.shortcuts import render_to_response
from theochempy._theochempy.Databases.Simple import DBAccess
from theochempy._theochempy.GraphDataModel import InfosetType
from theochempy._theochempy.GraphDataModel import InfosetTypeURI
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
   
    mol = _getMoleculeByMoleculeCode(db, mol_code)
    if mol is None:
        raise Http404
    
    infosets = mol.getInfosets()

    _createXYZFile(mol)

    render_data = { "dbname" : dbname, 
                    "molname" : str(mol.uuid()), 
                    "uuid" : str(mol.uuid())
                    }
    render_data["molecule"] = {}
    render_data["grrm"] = {}
    render_data["unrecognized"] = []

    for i in infosets:
        if i.type() == InfosetType.getMoleculeCodeType():
            render_data["molecule"]["MoleculeCode"] = i.value(None)
        elif i.typeURI() == InfosetTypeURI.INFOSET_TYPE_URI_BASE+"StructureType":
            render_data["grrm"]["StructureType"] = i.value(None)
        elif i.typeURI() == InfosetTypeURI.INFOSET_TYPE_URI_BASE+"Spin":
            render_data["grrm"]["Spin"] = i.value(None)
        elif i.typeURI() == InfosetTypeURI.INFOSET_TYPE_URI_BASE+"HFEnergy":
            render_data["grrm"]["HFEnergy"] = i.value(None)
        elif i.typeURI() == InfosetTypeURI.INFOSET_TYPE_URI_BASE+"ZeroPointVibrationalEnergy":
            render_data["grrm"]["ZeroPointVibrationalEnergy"] = i.value(None)
        elif i.typeURI() == InfosetTypeURI.INFOSET_TYPE_URI_BASE+"NormalModesEigenvalues":
            render_data["grrm"]["NormalModesEigenvalues"] = i.value(None)
        elif i.typeURI() == InfosetTypeURI.INFOSET_TYPE_URI_BASE+"ReactionConnectivityMarker":
            render_data["grrm"]["ReactionConnectivityMarker"] = i.value(None)
        elif i.typeURI() == InfosetTypeURI.INFOSET_TYPE_URI_BASE+"ReactionConnectivityCodes":
            render_data["grrm"]["ReactionConnectivityCodes"] = i.value(None)
            render_data["grrm"]["first_code"] = i.value(None)[0]
            render_data["grrm"]["second_code"] = i.value(None)[1]
        else:
            render_data["unrecognized"].append( ( i.typeURI(), i.dimensionality()))
    

    return render_to_response("application/browsemol.html", render_data )

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

def _getMoleculeByMoleculeCode(db, molecule_code):
    molecules = [x for x in db.retrieveAll()]

    for m in molecules:
        molecule_code_infoset = m.getInfosets(infoset_type=InfosetType.getMoleculeCodeType())
        if len(molecule_code_infoset) != 1:
            continue
        if molecule_code_infoset[0].value(None) == molecule_code:
            return m
   
    return None
