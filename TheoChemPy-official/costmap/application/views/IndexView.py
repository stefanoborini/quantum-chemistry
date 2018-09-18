from django.shortcuts import render_to_response
from theochempy._theochempy.Databases.Simple import DBAccess
from theochempy._theochempy.GraphDataModel import InfosetType
from theochempy._theochempy import Units
from django.http import Http404
from django.utils import simplejson
import settings
import os

def index(request):
    available_databases = []
    for d in os.listdir(settings.DB_PATH):
        try:
            db = DBAccess.DBAccess(os.path.join(settings.DB_PATH, d))
            name = os.path.basename(d)
            num_molecules = len(db.retrieveAll())
            comment = db.metainfo("comment")
            if comment is None:
                comment = "none"
            creation_date = db.metainfo("creation_date")
            if creation_date is None:
                creation_date = "Unknown"
        except:
            continue
        available_databases.append( { "name" : name, "num_molecules" : str(num_molecules), "comment" : comment, "creation_date" : creation_date })


    return render_to_response('application/index.html', { "available_databases" : available_databases }) 


