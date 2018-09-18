class InterconversionAdditionalInfo(object):
    def __init__(self,interconversion):
        self._interconversion = interconversion
        self._start_structure_label = None
        self._end_structure_label = None
    def interconversion(self):
        return self._interconversion
    def setStartStructureLabel(self,label):
        self._start_structure_label = label
    def setEndStructureLabel(self,label):
        self._end_structure_label = label
    def endStructureLabel(self):
        return self._end_structure_label
    def startStructureLabel(self):
        return self._start_structure_label

