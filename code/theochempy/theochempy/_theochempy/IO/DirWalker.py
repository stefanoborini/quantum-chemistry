#!/usr/bin/env python

import os

class ExtensionFilter:
    def __init__(self, allow):
        self._allow = allow

    def isAccepted(self, filename):
        name, ext = os.path.splitext(filename)
        if ext == "."+self._allow:
            return True
        return False

class NoFilter:
    def __init__(self):
        pass
    def isAccepted(self, filename):
        return True

class AndFilter:
    def __init__(self, filter1, filter2):
        self._filter1 = filter1
        self._filter2 = filter2
    def isAccepted(self, filename):
        return self._filter1.isAccepted(filename) and self._filter2.isAccepted(filename)

class TypeFilter:
    FILE="FILE"
    def __init__(self, allow):
        self._allow = allow

    def isAccepted(self, filename):
        if self._allow == TypeFilter.FILE:
            return os.path.isfile(filename)
        return False

class DirWalker:
    def __init__(self, start_path, filter=None):
        self._start_path = start_path
        if filter is None:
            self._filter = NoFilter()
        else:
            self._filter = filter
        self._list=_walk(start_path)
    def next(self):
        try:
            while True:
                element = self._list.pop(0)
                if self._filter.isAccepted(element):
                    return element
        except:
            raise StopIteration

    def __iter__(self):
        return self 


def _walk(start_dir):
    files = [start_dir]
    for entity in os.listdir(start_dir):
        path = os.path.join(start_dir,entity)
        if os.path.isfile(path):
            files.append(path)
        else:
            files.extend(_walk(path))

    return files

