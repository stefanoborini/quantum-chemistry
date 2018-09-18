jQuery.noConflict();

var wmdb = wmdb || {};

wmdb.initPaginator = function() {/*fold>>*/
    wmdb.paginator = new YAHOO.widget.Paginator({ rowsPerPage: 10, containers : [ "paginator", "paginator2" ] });
}/*<<fold*/

wmdb.filterFormFactory = function() {
        return {
            _current_id : 0,
            _available_filters : wmdb.filters.allFilters(),
            _filter_instances : {},
            addFilter : function(after_filter_id) {
                var after_filter_id = after_filter_id || null;
                var self = this;
                var current_id = this._newId();

                var html = "<li id=\"filter_"+current_id+"\"><a href=\"javascript:void(0);\" id=\"filter_"+current_id+"_add\">(+)</a>";
                if (after_filter_id != null) {
                    html += "<a href=\"javascript:void(0);\" id=\"filter_"+current_id+"_remove\">(-)</a>";
                } else {
                    html += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
                }
                html += "<select id=\"filter_"+current_id+"_selector\">";
                for (var i in this._available_filters) {
                    html += "<option value=\""+this._available_filters[i].typeId()+"\">"+this._available_filters[i].selectorLabel()+"</option>";
                } 
                html += "</select><span id=\"filter_"+current_id+"_content\">-</span>";
                html += "</li>";

                if (after_filter_id == null) {
                    jQuery("#search_form #filters").append(html);
                } else {
                    jQuery("#filter_"+after_filter_id).after(html);
                }
                jQuery("#filter_"+current_id+"_add").bind("click", function() { self.addFilter(current_id); }  );
                jQuery("#filter_"+current_id+"_remove").bind("click", function() { self.removeFilter(current_id); }  );
                jQuery("#filter_"+current_id+"_selector").bind("change", function() { self.selectorChanged(current_id); }  );

                this.selectorChanged(current_id);
            },
            show : function() {
                var self = this;
                jQuery("#filters").empty();
                this.addFilter();
            },
            setSubmitCallback : function(callback) {
                jQuery("#submit").bind("click", callback);
            },
            _newId : function() {
                this._current_id++;
                return this._current_id;
            },
            removeFilter : function(filter_id) {
                jQuery("#filter_"+filter_id).remove();
            },
            selectorChanged : function(filter_id) {
                var selected_id = jQuery("#filter_"+filter_id+"_selector").val();
                var filter_instance = wmdb.filters.filterFactory(selected_id,filter_id);
                jQuery("#filter_"+filter_id+"_content").empty().append(filter_instance.html());
                this._filter_instances[filter_id] = filter_instance;
            },
            queryUri : function() {
                var query = "";
                var li_entries = jQuery("#search_form li");
                var order = 0;
                for (var i = 0 ; i < li_entries.length; i++) {
                    var identifier = li_entries[i].id.substring(7);
                    var filter = this._filter_instances[identifier];
                    query += order+":"+filter.constructor.typeId()+":"+filter.httpGetParams()+",";
                    order+=1;
                }

                return query.substring(0,query.length-1);
                    
            },
        }
}

wmdb.doSubmit = function(e) {
    wmdb.initPaginator();
    wmdb.paginator.subscribe('changeRequest',wmdb.handlePageChange);
    jQuery.getJSON("/search/?type=ajax&filters="+encodeURIComponent(wmdb.filter_form.queryUri()), {}, wmdb.ajaxParseMatchingResources);
    return false;
}
wmdb.ajaxParseMatchingResources = function(data, status) {  
    for (var i = 0; i <10; i++) {
        jQuery("#result"+i).html("");
    }
    for (var i = 0; i < Math.min(10, data.uri_list.length); i++) {
        var callback = function(index) {
            return function(data, status, request) {
                var m = index;
                jQuery("#result"+m).html(data);
            }
        };
        jQuery.get("/searchsnippets/{"+data.uri_list[i].substring(9)+"}", callback(i));
    }
    wmdb.paginator.set('totalRecords',data.total);   
    wmdb.paginator.render();
}

wmdb.handlePageChange = function(new_state) {
    var paginator = wmdb.paginator;

    paginator.setState(new_state);

    var offset = (paginator.getCurrentPage() - 1) * 10;
    jQuery.getJSON("/search/?type=ajax&limit=10&offset="+offset+"&filters="+encodeURIComponent(wmdb.filter_form.queryUri()), {}, wmdb.ajaxParseMatchingResources);
}


jQuery(document).ready(function(){
    wmdb.filter_form = wmdb.filterFormFactory();
    wmdb.filter_form.show();
    wmdb.filter_form.setSubmitCallback(wmdb.doSubmit)

});


