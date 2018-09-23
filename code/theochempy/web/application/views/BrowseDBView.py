from django.shortcuts import render_to_response
from theochempy._theochempy.Databases.Simple import DBAccess
from theochempy._theochempy.GraphDataModel import InfosetType
from theochempy._theochempy import Units
from theochempy._theochempy.Chemistry import Utilities
from django.http import Http404
from django.utils import simplejson
import settings

import os

def browsedb(request,dbname):
    try:
        db = DBAccess.DBAccess(os.path.join(settings.DB_PATH, dbname))
    except:
        raise Http404

    molecule_list = []

    all = db.retrieveAll()
    molecule_list = []
    for graph in all:
        molecule={}
        code = graph.getInfosets(infoset_type=InfosetType.getMoleculeCodeType())
        if len(code) == 0:
            continue 
        else:
            molecule["code"] = code[0].value(graph)

        name = graph.getInfosets(infoset_type=InfosetType.getConventionalMoleculeNameType())
        if len(name) == 0:
            molecule["name"] = molecule["code"]
        else:
            molecule["name"] = name[0].value(graph)

        elements = graph.getInfosets(infoset_type=InfosetType.getElementType())
        if len(elements) == 0:
            continue
        else:
            molecule["num_of_atoms"] = elements[0].size()
            molecule["brute_formula"] = Utilities.hillFormula(map(lambda x: x[1], elements[0].allValues()))
        
        hf_energy = graph.getInfosets(infoset_type=InfosetType.getHFEnergyType())
        if len(hf_energy) == 0:
            continue
        else:
            molecule["hf_energy"] = hf_energy[0].value(graph)
            

        #molecule["uuid"] = graph.uuid()
        molecule_list.append(molecule)

    database = { "name": dbname }
    
    return render_to_response("application/browsedb.html", { "database" : database, "molecule_list" : molecule_list })


