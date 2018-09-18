from django.shortcuts import render_to_response
from theochempy._theochempy.Databases.Simple import DBAccess
from theochempy._theochempy.GraphDataModel import InfosetType
from theochempy._theochempy import Units
from django.http import Http404
from django.utils import simplejson

import os

def search(request):
    if request.POST is None or not request.POST.has_key("molecule_name"):
        return render_to_response("application/search.html")
    else:
        molecule_name = request.POST["molecule_name"]
        try:
            db = DBAccess.DBAccess(os.path.join(DB_PATH, "db"))
        except:
            raise Http404

        molecule_list = []

        all = db.retrieveAll()
        for graph in all:
            molecule={}
            names = graph.getInfosets(infoset_type=InfosetType.getConventionalMoleculeNameType())
            if len(names) == 0:
                molecule["name"] = graph.uuid()
            else:
                molecule["name"] = names[0].value(graph)
            if molecule["name"] == molecule_name:
                molecule_list.append(molecule)
    
        return render_to_response("application/browsedb.html", { "dbname" : "db", "molecule_list" : molecule_list })
    
