jQuery.noConflict();

if (typeof(wmdb) === "undefined") { var wmdb = {}; }
if (typeof(wmdb.filters) === "undefined") { wmdb.filters = {}; }

var baseenc = baseenc || {};

baseenc.b32encode = function(s) {
    /* encodes a string s to base32 and returns the encoded string */ 
    var alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";

    var parts = [];
    var quanta= Math.floor((s.length / 5));
    var leftover = s.length % 5;

    if (leftover != 0) {
        for (var i = 0; i < (5-leftover); i++) { s += '\x00'; }
        quanta += 1;
    }

    for (i = 0; i < quanta; i++) {
        parts.push(alphabet.charAt(s.charCodeAt(i*5) >> 3));
        parts.push(alphabet.charAt( ((s.charCodeAt(i*5) & 0x07) << 2) | (s.charCodeAt(i*5+1) >> 6)));
        parts.push(alphabet.charAt( ((s.charCodeAt(i*5+1) & 0x3F) >> 1) ));
        parts.push(alphabet.charAt( ((s.charCodeAt(i*5+1) & 0x01) << 4) | (s.charCodeAt(i*5+2) >> 4)));
        parts.push(alphabet.charAt( ((s.charCodeAt(i*5+2) & 0x0F) << 1) | (s.charCodeAt(i*5+3) >> 7)));
        parts.push(alphabet.charAt( ((s.charCodeAt(i*5+3) & 0x7F) >> 2)));
        parts.push(alphabet.charAt( ((s.charCodeAt(i*5+3) & 0x03) << 3) | (s.charCodeAt(i*5+4) >> 5)));
        parts.push(alphabet.charAt( ((s.charCodeAt(i*5+4) & 0x1F) )));
    }

    var replace = 0;
    if (leftover == 1) replace = 6;
    else if (leftover == 2) replace = 4;
    else if (leftover == 3) replace = 3;
    else if (leftover == 4) replace = 1;


    for (i = 0; i < replace; i++) parts.pop();
    for (i = 0; i < replace; i++) parts.push("=");

    return parts.join("");
}


wmdb.filters.GrrmTypeFilter = function(unique_id) { // fold>>
    this._unique_id = unique_id;
    this.html = function() {
        return ' is <select id="grrm__type_'+this._unique_id+'"><option value="grrm__equilibrium_structure" selected="selected">Equilibrium Structure</option><option value="grrm__transition_state">Transition State</option><option value="grrm__barrierless_dissociated">Barrierless Dissociated</option><option value="grrm__barrier_dissociated">Barrier Dissociated</option><option value="grrm__interconversion_step">Interconversion Step</option><option value="grrm__interconversion">Interconversion</option><option value="grrm__run">Run</option></select>';
    };
    this.httpGetParams = function() {
        var rdf_type = jQuery('#grrm__type_'+this._unique_id).val();
        return rdf_type;
    };
    this.uniqueId = function() {
        return this._unique_id;
    };
};
wmdb.filters.GrrmTypeFilter.typeId = function() { return "grrm__type"; };
wmdb.filters.GrrmTypeFilter.selectorLabel = function() { return "Resource type"; };
// <<fold

wmdb.filters.GrrmEnergyBetweenFilter = function(unique_id) { // fold>>
    this._unique_id = unique_id;
    this.html = function() {
        return ' <input type="text" id="grrm__energy_between_'+this._unique_id+'_lower" size="10"> and <input type="text" id="grrm__energy_between_'+this._unique_id+'_higher" size="10"> hartree';
    };
    this.httpGetParams = function() {
        var lower = jQuery("#grrm__energy_between_"+this._unique_id+"_lower").val();
        var higher = jQuery("#grrm__energy_between_"+this._unique_id+"_higher").val();
        return lower+":"+higher;
    };
    this.uniqueId = function() {
        return this._unique_id;
    };
};
wmdb.filters.GrrmEnergyBetweenFilter.typeId = function() { return "grrm__energy_between"; };
wmdb.filters.GrrmEnergyBetweenFilter.selectorLabel = function() { return "Energy is between "; };
// <<fold
wmdb.filters.GrrmCarbonsBetweenFilter = function(unique_id) { // fold>>
    this._unique_id = unique_id;
    this.html = function() {
        return ' <input type="text" id="grrm__carbons_between_'+this._unique_id+'_lower" size="3" maxlength="3"> and <input type="text" id="grrm__carbons_between_'+this._unique_id+'_higher" size="3" maxlength="3">';
    };
    this.httpGetParams = function() {
        var lower = jQuery("#grrm__carbons_between_"+this._unique_id+"_lower").val();
        var higher = jQuery("#grrm__carbons_between_"+this._unique_id+"_higher").val();
        return lower+":"+higher;
    };
    this.uniqueId = function() {
        return this._unique_id;
    };
};
wmdb.filters.GrrmCarbonsBetweenFilter.typeId = function() { return "grrm__carbons_between"; };
wmdb.filters.GrrmCarbonsBetweenFilter.selectorLabel = function() { return "Number of C atoms between "; };
// <<fold
wmdb.filters.GrrmHydrogensBetweenFilter = function(unique_id) { // fold>>
    this._unique_id = unique_id;
    this.html = function() {
        return ' <input type="text" id="grrm__hydrogens_between_'+this._unique_id+'_lower" size="3" maxlength="3"> and <input type="text" id="grrm__hydrogens_between_'+this._unique_id+'_higher" size="3" maxlength="3">';
    };
    this.httpGetParams = function() {
        var lower = jQuery("#grrm__hydrogens_between_"+this._unique_id+"_lower").val();
        var higher = jQuery("#grrm__hydrogens_between_"+this._unique_id+"_higher").val();
        return lower+":"+higher;
    };
    this.uniqueId = function() {
        return this._unique_id;
    };
};
wmdb.filters.GrrmHydrogensBetweenFilter.typeId = function() { return "grrm__hydrogens_between"; };
wmdb.filters.GrrmHydrogensBetweenFilter.selectorLabel = function() { return "Number of H atoms between "; };
// <<fold
wmdb.filters.GrrmNitrogensBetweenFilter = function(unique_id) { // fold>>
    this._unique_id = unique_id;
    this.html = function() {
        return ' <input type="text" id="grrm__nitrogens_between_'+this._unique_id+'_lower" size="3" maxlength="3"> and <input type="text" id="grrm__nitrogens_between_'+this._unique_id+'_higher" size="3" maxlength="3">';
    };
    this.httpGetParams = function() {
        var lower = jQuery("#grrm__nitrogens_between_"+this._unique_id+"_lower").val();
        var higher = jQuery("#grrm__nitrogens_between_"+this._unique_id+"_higher").val();
        return lower+":"+higher;
    };
    this.uniqueId = function() {
        return this._unique_id;
    };
};
wmdb.filters.GrrmNitrogensBetweenFilter.typeId = function() { return "grrm__nitrogens_between"; };
wmdb.filters.GrrmNitrogensBetweenFilter.selectorLabel = function() { return "Number of N atoms between "; };
// <<fold
wmdb.filters.GrrmOxygensBetweenFilter = function(unique_id) { // fold>>
    this._unique_id = unique_id;
    this.html = function() {
        return ' <input type="text" id="grrm__oxygens_between_'+this._unique_id+'_lower" size="3" maxlength="3"> and <input type="text" id="grrm__oxygens_between_'+this._unique_id+'_higher" size="3" maxlength="3">';
    };
    this.httpGetParams = function() {
        var lower = jQuery("#grrm__oxygens_between_"+this._unique_id+"_lower").val();
        var higher = jQuery("#grrm__oxygens_between_"+this._unique_id+"_higher").val();
        return lower+":"+higher;
    };
    this.uniqueId = function() {
        return this._unique_id;
    };
};
wmdb.filters.GrrmOxygensBetweenFilter.typeId = function() { return "grrm__oxygens_between"; };
wmdb.filters.GrrmOxygensBetweenFilter.selectorLabel = function() { return "Number of O atoms between "; };
// <<fold
wmdb.filters.GrrmSmilesFilter = function(unique_id) { // fold>>
    this._unique_id = unique_id;
    this.html = function() {
        return ' <input type="text" id="grrm__smiles_'+this._unique_id+'" size="20">';
    };
    this.httpGetParams = function() {
        var smiles = jQuery("#grrm__smiles_"+this._unique_id).val();
        return baseenc.b32encode(smiles);
    };
    this.uniqueId = function() {
        return this._unique_id;
    };
};
wmdb.filters.GrrmSmilesFilter.typeId = function() { return "grrm__smiles"; };
wmdb.filters.GrrmSmilesFilter.selectorLabel = function() { return "SMILES is exactly "; };
// <<fold
wmdb.filters.GrrmInchiFilter = function(unique_id) { // fold>>
    this._unique_id = unique_id;
    this.html = function() {
        return ' <input type="text" id="grrm__inchi_'+this._unique_id+'" size="20">';
    };
    this.httpGetParams = function() {
        var inchi = jQuery("#grrm__inchi_"+this._unique_id).val();
        return baseenc.b32encode(inchi);
    };
    this.uniqueId = function() {
        return this._unique_id;
    };
};
wmdb.filters.GrrmInchiFilter.typeId = function() { return "grrm__inchi"; };
wmdb.filters.GrrmInchiFilter.selectorLabel = function() { return "InChi is exactly "; };
// <<fold
wmdb.filters.GrrmCanostPlanarFilter = function(unique_id) { // fold>>
    this._unique_id = unique_id;
    this.html = function() {
        return ' <input type="text" id="grrm__canost_planar_'+this._unique_id+'" size="20">';
    };
    this.httpGetParams = function() {
        var canost = jQuery("#grrm__canost_planar_"+this._unique_id).val();
        return baseenc.b32encode(canost);
    };
    this.uniqueId = function() {
        return this._unique_id;
    };
};
wmdb.filters.GrrmCanostPlanarFilter.typeId = function() { return "grrm__canost_planar"; };
wmdb.filters.GrrmCanostPlanarFilter.selectorLabel = function() { return "Canost Planar is exactly "; };
// <<fold
wmdb.filters.GrrmBasisSetFilter = function(unique_id) { // fold>>
    this._unique_id = unique_id;
    this.html = function() {
        return ' <input type="text" id="grrm__basis_set_'+this._unique_id+'" size="20">';
    };
    this.httpGetParams = function() {
        var smiles = jQuery("#grrm__basis_set_"+this._unique_id).val();
        return smiles;
    };
    this.uniqueId = function() {
        return this._unique_id;
    };
};
wmdb.filters.GrrmBasisSetFilter.typeId = function() { return "grrm__basis_set"; };
wmdb.filters.GrrmBasisSetFilter.selectorLabel = function() { return "Basis set is "; };
// <<fold
wmdb.filters.GrrmMassBetweenFilter = function(unique_id) { // fold>>
    this._unique_id = unique_id;
    this.html = function() {
        return ' <input type="text" id="grrm__mass_between_'+this._unique_id+'_lower" size="10"> and <input type="text" id="grrm__mass_between_'+this._unique_id+'_higher" size="10"> dalton';
    };
    this.httpGetParams = function() {
        var lower = jQuery("#grrm__mass_between_"+this._unique_id+"_lower").val();
        var higher = jQuery("#grrm__mass_between_"+this._unique_id+"_higher").val();
        return lower+":"+higher;
    };
    this.uniqueId = function() {
        return this._unique_id;
    };
};
wmdb.filters.GrrmMassBetweenFilter.typeId = function() { return "grrm__mass_between"; };
wmdb.filters.GrrmMassBetweenFilter.selectorLabel = function() { return "Mass is between "; };
// <<fold

wmdb.filters.allFilters = function() { return [ wmdb.filters.GrrmTypeFilter, 
                             wmdb.filters.GrrmEnergyBetweenFilter,
                             wmdb.filters.GrrmCarbonsBetweenFilter,
                             wmdb.filters.GrrmNitrogensBetweenFilter,
                             wmdb.filters.GrrmHydrogensBetweenFilter,
                             wmdb.filters.GrrmOxygensBetweenFilter,
                             wmdb.filters.GrrmSmilesFilter,
                             wmdb.filters.GrrmInchiFilter,
                             wmdb.filters.GrrmCanostPlanarFilter,
                             wmdb.filters.GrrmBasisSetFilter,
                             wmdb.filters.GrrmMassBetweenFilter,
                            ];
}

wmdb.filters.filterFactory = function(type_id, unique_id) {
    var all_filters = wmdb.filters.allFilters();
    for (var i in all_filters) {
        if (type_id === all_filters[i].typeId()) {
            return new all_filters[i](unique_id);
        }
    }
};

