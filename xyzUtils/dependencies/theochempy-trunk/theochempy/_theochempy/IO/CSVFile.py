import csv

class CSVFile:
    """Class to load and manipulate CSV data.
    Please note that the size of the data is given by the highest indexes of the data stored.
    Every get operation which tries to access data (or operation that has to read data from the matrix in some way) beyond the size will raise IndexError.
    Every purely setting operation which tries to access data beyond the size will instead enlarge the 
    csv matrix so to accomodate the new data.
    Note also that an empty string is equivalent to no value.
    """
    def __init__(self, filename = None): # fold>>
        self._entries = {}
        self._num_of_rows = 0
        self._num_of_cols = 0

        if filename is None:
            return 
        f=file(filename,"r")
        csv_reader = csv.reader(f, dialect='excel')

        row_index = 0
        for row in csv_reader:
            if len(row[0].strip()) == 0 or row[0].strip()[0] == "#":
                continue
            for column_index, entry in enumerate(row):
                self._entries[(row_index, column_index)] = str(entry)
            row_index += 1
        f.close()
        self._updateSize()

# <<fold
    def _updateSize(self): # fold>>
        # terribly inefficient. Who cares for now.
        self._num_of_rows=0
        self._num_of_cols=0
        for key in self._entries.keys():
            self._num_of_rows = max(self._num_of_rows, key[0])
            self._num_of_cols = max(self._num_of_cols, key[1])
        self._num_of_rows+=1
        self._num_of_cols+=1

# <<fold

    def getColumn(self, index): # fold>>
        if index >= self._num_of_cols or index < 0:
            raise IndexError()
        column = []
        for row_index in xrange(0, self._num_of_rows):
            column.append(self._entries.get((row_index, index), ""))
        return column

# <<fold
    def getRow(self, index):  # fold>>
        if index >= self._num_of_rows or index < 0:
            raise IndexError()
        row = []
        for column_index in xrange(0, self._num_of_cols):
            row.append(self._entries.get((index, column_index), ""))
        return row

# <<fold
    def getNumOfRows(self): # fold>>
        return self._num_of_rows

# <<fold
    def getNumOfColumns(self): # fold>>
        return self._num_of_cols

# <<fold

    def swapRows(self, first, second): # fold>>
        if first >= self._num_of_rows or first < 0 or second >= self._num_of_rows or second < 0:
            raise IndexError()
        for column_index in xrange(0, self._num_of_cols):
            if not self._entries.has_key((first, column_index)) and not self._entries.has_key((second, column_index)):
                continue
            elif self._entries.has_key((first, column_index)) and not self._entries.has_key((second, column_index)):
                self._entries[(second, column_index)] = self._entries[(first, column_index)]
                del self._entries[(first, column_index)]
            elif not self._entries.has_key((first, column_index)) and self._entries.has_key((second, column_index)):
                self._entries[(first, column_index)] = self._entries[(second, column_index)]
                del self._entries[(second, column_index)]
            else:
                self._entries[(first, column_index)], self._entries[(second, column_index)] = self._entries[(second, column_index)], self._entries[(first, column_index)]
                
                # <<fold
    def swapColumns(self, first, second): # fold>>
        if first >= self._num_of_cols or first < 0 or second >= self._num_of_cols or second < 0:
            raise IndexError()
        for row_index in xrange(0, self._num_of_rows):
            if not self._entries.has_key((row_index, first)) and not self._entries.has_key((row_index, second)):
                continue
            elif self._entries.has_key((row_index, first)) and not self._entries.has_key((row_index, second)):
                self._entries[(row_index, second)] = self._entries[(row_index, first)]
                del self._entries[(row_index, first)]
            elif not self._entries.has_key((row_index, first)) and self._entries.has_key((row_index, second)):
                self._entries[(row_index, first)] = self._entries[(row_index, second)]
                del self._entries[(row_index, second)]
            else:
                self._entries[(row_index, first)], self._entries[(row_index, second)] = self._entries[(row_index, second)], self._entries[(row_index, first)]

# <<fold
    def applyToColumn(self, index, func, *func_args):  # fold>>
        if index >= self._num_of_cols or index < 0:
            raise IndexError()

        for row_index in xrange(0, self._num_of_rows):
            new_val = func(self._entries.get( (row_index, index), ""), row_index, *func_args)
            if new_val is None:
                del self._entries[(row_index, index)]
            else:
                self._entries[(row_index, index)]=str(new_val)
        
        # <<fold
    def applyToRow(self, index, func, *func_args): # fold>>
        if index >= self._num_of_rows or index < 0:
            raise IndexError()

        for column_index in xrange(0, self._num_of_cols):
            new_val = func(self._entries.get( (index, column_index), "") , column_index, *func_args)
            if new_val is None:
                del self._entries[(index, column_index)]
            else:
                self._entries[(index, column_index)]=str(new_val)

# <<fold
    def getValue(self, row, column): # fold>>
        if row >= self._num_of_rows or row < 0 or column >= self._num_of_cols or column < 0:
            raise IndexError()

        return self._entries.get((row, column), "")

# <<fold
    def setValue(self, row, column, value): # fold>>
        if value is None or len(str(value)) == 0:
            try:
                del self._entries[(row, column)]
            except KeyError:
                pass
        else:
            self._entries[(row,column)] = str(value)
        self._updateSize()
# <<fold
    def insertColumn(self, index, column): # fold>>
        # move all the stuff forward. Not very efficient, but for now it will do it.

        for column_index in xrange(self._num_of_cols-1, index-1, -1):
            for row_index in xrange(0, self._num_of_rows):
                if self._entries.has_key((row_index, column_index)):
                    self._entries[(row_index, column_index+1)] = self._entries[(row_index, column_index)]
                else:
                    try:
                        del self._entries[(row_index, column_index+1)]
                    except KeyError:
                        pass
        # insert new
        for row_index, entry in enumerate(column):
            self._entries[(row_index, index)] = str(entry)

        self._updateSize()

# <<fold
    def insertRow(self, index, row):  # fold>>

        # move all the stuff forward. Not very efficient, but for now it will do it.
        for row_index in xrange(self._num_of_rows-1, index-1, -1):
            for column_index in xrange(0, self._num_of_cols):
                if self._entries.has_key((row_index, column_index)):
                    self._entries[(row_index+1, column_index)] = self._entries[(row_index, column_index)]
                else:
                    try:
                        del self._entries[(row_index+1, column_index)]
                    except KeyError:
                        pass
        # insert new
        for column_index, entry in enumerate(row):
            self._entries[(index,column_index)] = str(entry)

        self._updateSize()

# <<fold
    def removeRow(self, index): # fold>>
        if index >= self._num_of_rows or index < 0:
            raise IndexError()

        for column_index in xrange(0, self._num_of_cols):
            try:
                del self._entries[(index, column_index)]
            except KeyError:
                pass

        for row_index in xrange(index+1, self._num_of_rows):
            for column_index in xrange(0, self._num_of_cols):
                if self._entries.has_key((row_index, column_index)):
                    self._entries[(row_index-1, column_index)] = self._entries[(row_index, column_index)]
                else:
                    try:
                        del self._entries[(row_index-1, column_index)]
                    except KeyError:
                        pass

        for column_index in xrange(0, self._num_of_cols):
            try:
                del self._entries[(self._num_of_rows-1, column_index)]
            except KeyError:
                pass

        self._updateSize()
        # <<fold
    def removeColumn(self, index): # fold>>
        if index >= self._num_of_cols or index < 0:
            raise IndexError()

        for row_index in xrange(0, self._num_of_rows):
            try:
                del self._entries[(row_index, index)]
            except KeyError:
                pass

        for column_index in xrange(index+1, self._num_of_cols):
            for row_index in xrange(0, self._num_of_rows):
                if self._entries.has_key((row_index, column_index)):
                    self._entries[(row_index, column_index-1)] = self._entries[(row_index, column_index)]
                else:
                    try:
                        del self._entries[(row_index, column_index-1)]
                    except KeyError:
                        pass

        for row_index in xrange(0, self._num_of_rows):
            try:
                del self._entries[(row_index, self._num_of_cols-1)]
            except KeyError:
                pass

        self._updateSize() 
        # <<fold
    def saveTo(self, filename):  # fold>>
        f=file(filename,"w")
        csv_writer = csv.writer(f, dialect='excel')
        for row_index in xrange(self._num_of_rows):
            row = []
            for col_index in xrange(self._num_of_cols):
                row.append(str( self._entries.get( (row_index, col_index), "")) )

            csv_writer.writerow(row)
        f.close()

        # <<fold
