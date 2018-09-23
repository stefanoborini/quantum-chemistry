from . import elements

import types

class PeriodicTable(object):
    """PeriodicTable contains access point routines to obtain elements.
    It must not be instantiated by the user.
    It returns objects of type elements.Element, representing element data according to 
    IUPAC tech reports 2007 (Pure Appl. Chem., Vol. 81, No. 11, pp.2131-2156, 2009.
    doi:10.1351/PAC-REP-09-08-03)
    """
    def __init__(self):
        raise Exception("PeriodicTable object cannot be instantiated")
    @staticmethod
    def element(**args):
        """Return an element corresponding to the given symbol or atomic number.
        Accepted parameters: symbol, atomic_number
        """
        if len(args) != 1:
            raise TypeError("This routine accepts a single argument")

        if args.get("symbol"):
            symbol = args["symbol"]
            for e in elements.all():
                if e.symbol() == symbol:
                    return e
            return None
        elif args.get("atomic_number"):
            atnum = args["atomic_number"]
            for e in elements.all():
                if e.atomicNumber() == atnum:
                    return e
            return None


def hillFormula(element_list):
    "Returns the Hill's formula out of a list of Element objects, symbols, or atomic numbers"
    brute = {}
    
    def _coerceToElement(something):
        if isinstance(something,elements.Element):
            element=something
        elif isinstance(something, int):
            element=PeriodicTable.element(atomic_number=something)
        elif isinstance(something, str):
            element=PeriodicTable.element(symbol=something)
        else:
            element=None
        if not element:
            raise TypeError("unable to coerce to element")
        return element

    for element in [ _coerceToElement(x) for x in element_list]:
        symbol = element.symbol()
            
        if brute.has_key(symbol):
            brute[symbol] += 1
        else:
            brute[symbol] = 1

    brute_string = ""
    if brute.has_key("C"):
        brute_string = brute_string + "C"
        if brute["C"] > 1:
            brute_string+=str(brute["C"])
        del brute["C"]

        if brute.has_key("H"):
            brute_string = brute_string + "H"
            if brute["H"] > 1:
                brute_string+=str(brute["H"])
            del brute["H"]

    for key, value in sorted(brute.items()):
        brute_string+=str(key)
        if value > 1:
            brute_string+=str(value)

    return brute_string

