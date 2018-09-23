# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../"));
import unittest

from theochempy._theochempy.IO import CSVFile

def moduleDir():
    return os.path.dirname(__file__)

    
class TestCSVFile(unittest.TestCase):
    def testInit(self): # fold>>
        csv = CSVFile.CSVFile(os.path.join(moduleDir(),"testfile.csv"))
        self.assertEqual(csv.__class__, CSVFile.CSVFile)
        # <<fold
    def testInit2(self): # fold>>
        csv = CSVFile.CSVFile()
        self.assertEqual(csv.__class__, CSVFile.CSVFile)
        # <<fold
    def testInsertRow(self): # fold>>
        csv = CSVFile.CSVFile(os.path.join(moduleDir(),"testfile.csv") )

        self.assertEqual(len(csv.getColumn(0)), 5)

        csv.insertRow(0,[1,2,3,4])
        self.assertEqual(len(csv.getColumn(0)), 6)
        # <<fold 
    def testInsertRowEmpty1(self): # fold>>
        csv = CSVFile.CSVFile()
        csv.insertRow(0,[1,2,3,4])

        self.assertEqual(len(csv.getColumn(0)), 1)
        self.assertEqual(len(csv.getRow(0)), 4)
        self.assertEqual(csv.getNumOfRows(),1)
        # <<fold 
    def testInsertRowEmpty2(self): # fold>>
        csv = CSVFile.CSVFile()
        csv.insertRow(3,[1,2,3,4])

        self.assertEqual(len(csv.getColumn(0)), 4)
        self.assertEqual(csv.getColumn(0)[0], "")
        self.assertEqual(csv.getColumn(0)[1], "")
        self.assertEqual(csv.getColumn(0)[2], "")
        self.assertEqual(csv.getColumn(0)[3], "1")
        self.assertEqual(csv.getNumOfRows(),4)
        # <<fold 
    def testGetColumn(self): # fold>>
        csv = CSVFile.CSVFile(os.path.join(moduleDir(),"testfile.csv"), )
        
        self.assertEqual(len(csv.getColumn(0)), 5)
        self.assertEqual(csv.getColumn(0), ["1","2","3","10","11"])
        self.assertEqual(csv.getColumn(3), ["10.0","20.0","30.0","1.0","hello"])
        self.assertRaises(IndexError, csv.getColumn, 4)
        # <<fold
    def testGetNumOfColumns(self): # fold>>
        csv = CSVFile.CSVFile(os.path.join(moduleDir(),"testfile.csv"), )
        
        self.assertEqual(csv.getNumOfColumns(), 4)
        
        # <<fold
    def testGetNumOfRows(self): # fold>>
        csv = CSVFile.CSVFile(os.path.join(moduleDir(),"testfile.csv"))
        
        self.assertEqual(csv.getNumOfRows(), 5)
        
        # <<fold
    def testSwapColumns(self): # fold>>
        csv = CSVFile.CSVFile(os.path.join(moduleDir(),"testfile.csv"), )
       
        csv.swapColumns(0,1)
        column = csv.getColumn(1)
        self.assertEqual(column[0], "1")
        self.assertEqual(column[1], "2")
        self.assertEqual(column[2], "3")
        self.assertEqual(column[3], "10")
        self.assertEqual(column[4], "11")

        column = csv.getColumn(0)
        self.assertEqual(column[0], "hello")
        self.assertEqual(column[1], " hello ")
        self.assertEqual(column[2], " hello ")
        self.assertEqual(column[3], "")
        self.assertEqual(column[4], "")

        self.assertRaises(IndexError, csv.swapColumns, 1, 10) 
        
        # <<fold
    def testSwapRows(self): # fold>>
        csv = CSVFile.CSVFile(os.path.join(moduleDir(),"testfile.csv"), )
       
        csv.swapRows(0,1)
       
        row = csv.getRow(1)
        self.assertEqual(row[0], "1")
        self.assertEqual(row[1], "hello")
        self.assertEqual(row[2], "3")
        self.assertEqual(row[3], "10.0")

        row = csv.getRow(0)
        self.assertEqual(row[0], "2")
        self.assertEqual(row[1], " hello ")
        self.assertEqual(row[2], "3")
        self.assertEqual(row[3], "20.0")

        self.assertRaises(IndexError, csv.swapRows, 1, 10) 
        # <<fold
    def testApplyToColumn(self): # fold>>
        csv = CSVFile.CSVFile(os.path.join(moduleDir(),"testfile.csv"), )
        
        def add(value, current_index, *func_args):
            return str(float(value) + func_args[0])

        csv.applyToColumn(0,add, 5.0)

        column = csv.getColumn(0)
        self.assertEqual(column[0], "6.0")
        self.assertEqual(column[1], "7.0")
        self.assertEqual(column[2], "8.0")
        self.assertEqual(column[3], "15.0")
        self.assertEqual(column[4], "16.0")


        # <<fold
    def testApplyToRow(self): # fold>>
        csv = CSVFile.CSVFile(os.path.join(moduleDir(),"testfile.csv"), )

        def addIfPossible(value, current_index, *args):
            try:
                v=float(value)
            except:
                return value
            return str(v + args[0][current_index])
       
        csv.applyToRow(0,addIfPossible, [1,2,3,4])

        row = csv.getRow(0)
        self.assertEqual(row[0],"2.0")
        self.assertEqual(row[1],"hello")
        self.assertEqual(row[2],"6.0")
        self.assertEqual(row[3],"14.0")
        # <<fold
    def testGetValue(self): # fold>>
        csv = CSVFile.CSVFile(os.path.join(moduleDir(),"testfile.csv") )
        self.assertEqual(csv.getValue(0,0), "1")
        self.assertEqual(csv.getValue(1,1), " hello ")
        # <<fold 
    def testSetValue(self): # fold>>
        csv = CSVFile.CSVFile(os.path.join(moduleDir(),"testfile.csv"), )
        csv.setValue(3,3, "10.0")
        self.assertEqual(csv.getValue(3,3),"10.0")
        
        # <<fold
    def testInsertColumn(self): # fold>>
        csv = CSVFile.CSVFile(os.path.join(moduleDir(),"testfile.csv") )
        csv.insertColumn(0, [1,2,3,4,5])

        self.assertEqual(len(csv.getRow(0)), 5)

        # <<fold
    def testRemoveColumn(self): # fold>>
        csv = CSVFile.CSVFile(os.path.join(moduleDir(),"testfile.csv") )
        csv.removeColumn(0)
        self.assertEqual(len(csv.getRow(0)), 3)
        
        # <<fold
    def testRemoveRow(self): # fold>>
        csv = CSVFile.CSVFile(os.path.join(moduleDir(),"testfile.csv") )
        csv.removeRow(0)
        self.assertEqual(len(csv.getColumn(0)), 4)
        # <<fold
    def testSave(self): # fold>>
        csv = CSVFile.CSVFile()
        csv.insertColumn(0,[1,2,3])
        csv.insertColumn(1,[3,4,5])
        csv.insertColumn(2,["hello",4,5])
        csv.saveTo(os.path.join(moduleDir(),"new_testfile.csv") )

        csv = CSVFile.CSVFile(os.path.join(moduleDir(),"new_testfile.csv"))
        self.assertEqual(csv.getColumn(0), ["1","2","3"])
        self.assertEqual(csv.getColumn(1), ["3","4","5"])
        self.assertEqual(csv.getColumn(2), ["hello","4","5"])

    # <<fold

if __name__ == '__main__':
    unittest.main()
