def hillFormula(element_list):
    "Returns the Hill's formula out of a list of Element objects"
    brute = {}

    for element in element_list:
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

