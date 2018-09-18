var wmdb = wmdb || {};
wmdb.plugins = wmdb.plugins || {};
wmdb.plugins.runoutput = wmdb.plugins.runoutput || {};
wmdb.plugins.runoutput.paginator = null;
wmdb.plugins.runoutput.myDataTable = null; 
wmdb.plugins.runoutput.resource_uuid = null;

wmdb.plugins.runoutput.init = function(resource_uuid) {
    wmdb.plugins.runoutput.resource_uuid = resource_uuid;
    wmdb.plugins.runoutput.initDataTable();
    wmdb.plugins.runoutput.initPaginator();
    wmdb.plugins.runoutput.loadFirstData();
}
wmdb.plugins.runoutput.initDataTable = function() {/*fold>>*/
    var source = new YAHOO.util.DataSource(YAHOO.util.Dom.get("myTable"));
    source.responseType = YAHOO.util.DataSource.TYPE_HTMLTABLE;
    source.responseSchema = {
        fields: [{key:"id", parser:"number"},
        ]
    };
    var myColumnDefs = [
        {key:"icon", label: "Icon", width: 64 },
        {key:"id", label: "ID", width: 350, formatter: function(elCell, oRecord, oColumn, oData) { elCell.innerHTML = "<pre>"+oData+"</pre>"; } },
        {key:"type", label: "Type", width: 150 },
    ];

    wmdb.plugins.runoutput.myDataTable = new YAHOO.widget.DataTable("myMarkedUpContainer", myColumnDefs, source, { paginator: wmdb.plugins.runoutput.paginator });
}/*<<fold*/
wmdb.plugins.runoutput.initPaginator = function() {/*fold>>*/
    wmdb.plugins.runoutput.paginator = new YAHOO.widget.Paginator({ rowsPerPage: 10, containers : [ "paginator", "paginator2" ] });
    wmdb.plugins.runoutput.paginator.render();
}/*<<fold*/

wmdb.plugins.runoutput.ajaxParseMatchingResources = function(data, status) {
    var datatable = wmdb.plugins.runoutput.myDataTable;

    datatable.deleteRows(0, datatable.getRecordSet().getLength()); 

    for (var idx = 0; idx < data.uri_list.length; idx++) {
        var uuid = data.uri_list[idx].substring(9);
        datatable.addRow({ id: "<a href=\"/resources/%7B"+uuid+"%7D\">"+data.uri_list[idx]+"</a>", 
                           icon: "<a href=\"/resources/%7B"+uuid+"%7D\"><img id=\"icon_"+idx+"\" src=\"/cache/resources/"+uuid+"/animatedicon_"+uuid+".gif\"/></a>",
                            type: data.resource_type[idx],
                         }, idx);
    }
    datatable.get("paginator").set('totalRecords',data.total);


}

wmdb.plugins.runoutput.loadFirstData = function() {
    var resource_uuid = wmdb.plugins.runoutput.resource_uuid;
    jQuery.getJSON("/resources/%7B"+resource_uuid+"%7D?type=ajax&receiver_plugin=runoutput&method=getUris&limit=10&offset=0", {}, wmdb.plugins.runoutput.parseFirstData);
}

wmdb.plugins.runoutput.parseFirstData = function(data, status) {
    var paginator = wmdb.plugins.runoutput.paginator;
    paginator.set('totalRecords',data.total);
    paginator.subscribe('changeRequest',wmdb.plugins.runoutput.handlePageChange);
    var datatable = wmdb.plugins.runoutput.myDataTable;

    datatable.deleteRows(0, datatable.getRecordSet().getLength()); 

    for (var idx = 0; idx < data.uri_list.length; idx++) {
        var uuid = data.uri_list[idx].substring(9);
        datatable.addRow({ id: "<a href=\"/resources/%7B"+uuid+"%7D\">"+data.uri_list[idx]+"</a>", 
                           icon: "<a href=\"/resources/%7B"+uuid+"%7D\"><img id=\"icon_"+idx+"\" src=\"/cache/resources/"+uuid+"/animatedicon_"+uuid+".gif\"/></a>",
                            type: data.resource_type[idx],
                         }, idx);
    }
}

wmdb.plugins.runoutput.handlePageChange = function(new_state) {
    var paginator = wmdb.plugins.runoutput.paginator;
    var datatable = wmdb.plugins.runoutput.myDataTable;
    paginator.setState(new_state);

    datatable.deleteRows(0, datatable.getRecordSet().getLength()); 

    var offset = (paginator.getCurrentPage() - 1) * 10;
    var resource_uuid = wmdb.plugins.runoutput.resource_uuid;
    jQuery.getJSON("/resources/%7B"+resource_uuid+"%7D?type=ajax&receiver_plugin=runoutput&method=getUris&limit=10&offset="+offset, {}, wmdb.plugins.runoutput.fillDataTable);
}


wmdb.plugins.runoutput.fillDataTable = function(data, status) {
    var datatable = wmdb.plugins.runoutput.myDataTable;

    datatable.deleteRows(0, datatable.getRecordSet().getLength()); 

    for (var idx = 0; idx < data.uri_list.length; idx++) {
        var uuid = data.uri_list[idx].substring(9);
        datatable.addRow({ id: "<a href=\"/resources/%7B"+uuid+"%7D\">"+data.uri_list[idx]+"</a>", 
                           icon: "<a href=\"/resources/%7B"+uuid+"%7D\"><img id=\"icon_"+idx+"\" src=\"/cache/resources/"+uuid+"/animatedicon_"+uuid+".gif\"/></a>",
                            type: data.resource_type[idx],
                         }, idx);
    }
}
