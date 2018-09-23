def product(L,*lists):
    if not lists:
        for x in L:
            yield (x,)
    else:
        for x in L:
            for y in product(lists[0],*lists[1:]):
                yield (x,)+y

