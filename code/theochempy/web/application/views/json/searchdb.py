from theochempy._theochempy.Databases.Simple import DBAccess
from theochempy._theochempy.GraphDataModel import InfosetType
from theochempy._theochempy.Chemistry import Utilities
from theochempy._theochempy import Units
from django.http import Http404, HttpResponse
from django.utils import simplejson
import settings

import os

def compareRowsByCode(r0, r1): return cmp(r0["cell"][0], r1["cell"][0])
def compareRowsByConventionalName(r0, r1): return cmp(r0["cell"][1], r1["cell"][1])
def compareRowsByChemicalFormula(r0, r1): return cmp(r0["cell"][2], r1["cell"][2])
def compareRowsByNumOfAtoms(r0, r1): return cmp(int(r0["cell"][3]), int(r1["cell"][3]))
def compareRowsByHFEnergy(r0, r1): return cmp(r0["cell"][4], r1["cell"][4])
def compareRowsByCreationDate(r0, r1): return cmp(r0["cell"][5], r1["cell"][5])

def sortAndTrim(rows, page, rows_per_page, sortname, sortorder):
    if sortname == "code":
        sortfunc = compareRowsByCode
    elif sortname == 'conventional_name':
        sortfunc = compareRowsByConventionalName
    elif sortname == 'chemical_formula':
        sortfunc = compareRowsByChemicalFormula
    elif sortname == 'num_of_atoms':
        sortfunc = compareRowsByNumOfAtoms
    elif sortname == 'creation_date':
        sortfunc = compareRowsByCreationDate
    elif sortname == 'hf_energy':
        sortfunc = compareRowsByHFEnergy
    else:
        raise Http404 # FIXME change to 400

    rows.sort(cmp=sortfunc)
    if sortorder == "desc":
        rows.reverse()
    return rows[(page-1)*rows_per_page:(page-1)*rows_per_page+rows_per_page+1]

def searchdb(request):
    if request.method == "POST" and request.POST:
        db_name = request.POST["db_name"]
        page = int(request.POST['page'])
        rows_per_page = int(request.POST['rp'])
        sortname = request.POST['sortname']
        sortorder = request.POST['sortorder']
    else:
        raise Http404

    try:
        db = DBAccess.DBAccess(os.path.join(settings.DB_PATH, db_name))
    except:
        raise Http404

    all = db.retrieveAll()

    json_response = { "page": page, 
                      "total": len(all), 
                      "rows" : []
                    }
    rows = []
    for id, graph in enumerate(all):
        molecule = {}

        code = graph.getInfosets(infoset_type=InfosetType.getMoleculeCodeType())
        if len(code) == 0:
            continue 
        else:
            # FIXME possible danger of injection of db_name by the user
            molecule["code"] = "<a href=\"/browsedb/"+db_name+"/"+code[0].value(graph)+"\">"+code[0].value(graph)+"</a>"

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
            molecule["hf_energy"] = ""
        else:
            molecule["hf_energy"] = hf_energy[0].value(graph).value()


        row = {}
        row["id"] = molecule["code"]
        row["cell"] = [ molecule["code"], molecule["name"], molecule["brute_formula"], molecule["num_of_atoms"], molecule["hf_energy"],"" ]
        rows.append(row)
     
    json_response["rows"].extend(sortAndTrim(rows, page, rows_per_page, sortname, sortorder))


    return HttpResponse(simplejson.dumps(json_response), mimetype='application/javascript')



#function runSQL($rsql) {
#
#function countRec($fname,$tname) {
#$sql = "SELECT count($fname) FROM $tname ";
#$result = runSQL($sql);
#while ($row = mysql_fetch_array($result)) {
##return $row[0];
#}
#}
#
#$page = $_POST['page'];
#$rp = $_POST['rp'];
#$sortname = $_POST['sortname'];
#$sortorder = $_POST['sortorder'];
#
#if (!$sortname) $sortname = 'name';
#if (!$sortorder) $sortorder = 'desc';
#
#$sort = "ORDER BY $sortname $sortorder";
#
#if (!$page) $page = 1;
#if (!$rp) $rp = 10;
#
#$start = (($page-1) * $rp);
#
#$limit = "LIMIT $start, $rp";
#
#$sql = "SELECT iso,name,printable_name,iso3,numcode FROM country $sort $limit";
#$result = runSQL($sql);
#
#$total = countRec('iso','country');
#
#
#
#
##def ajax_example(request):
    #response_dict = {}
    #name = request.POST.get('name', False)
    #total = request.POST.get('total', False)
    #response_dict.update({'name': name, 'total': total})
    #if total:
        #try:
            #total = int(total)
        #except:
            #total = False
    #if name and total and int(total) == 10:
        #response_dict.update({'success': True})
    #else:
        #response_dict.update({'errors': {}})
        #if not name:
            #response_dict['errors'].update({'name': 'This field is required'})
        #if not total and total is not False:
            #response_dict['errors'].update({'total': 'This field is required'})
        #elif int(total) != 10:
            #response_dict['errors'].update({'total': 'Incorrect total'})
    #if xhr:
        #return HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    #return render_to_response('weblog/ajax_example.html', response_dict)
#
