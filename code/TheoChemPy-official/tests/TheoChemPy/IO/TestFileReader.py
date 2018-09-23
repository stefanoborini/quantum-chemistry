# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../"));
import unittest
import tempfile

from TheoChemPy.IO import FileReader

def moduleDir():
    return os.path.dirname(__file__)

    
class TestFileReader(unittest.TestCase):
    def testFileReaderOpen(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        
        self.assertEqual(f.__class__, FileReader.FileReader)
        f.close()
        # <<fold
    def testFileReadLine(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))

        l = f.readline()
        self.assertEqual(l,"1st line\n")
        l = f.readline()
        self.assertEqual(l,"2nd line\n")
        l = f.readline()
        self.assertEqual(l,"3rd line\n")

        # now the pointer is at end of file
        self.assertEqual(f.readline(), '')
        f.close()
        # <<fold

    def testLen(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        self.assertEqual(len(f),3)
        f.close()
        # <<fold
    def testGetItem(self): # fold>>
         
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        
        self.assertEqual(f[0],"1st line\n")
        self.assertEqual(f[1],"2nd line\n")
        self.assertEqual(f[2],"3rd line\n")
        f.close()
        # <<fold


    def testGetItemOutOfBounds(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))

        # move at BOF with big negative num
        self.assertEqual(f[-999999],'')
        self.assertEqual(f.isAtBOF(), True)
        # move at EOF with big positive num
        self.assertEqual(f[9999999], '')
        self.assertEqual(f.isAtEOF(), True)
        # move at BOF with -1
        self.assertEqual(f[-1], '')
        self.assertEqual(f.isAtBOF(), True)
        # move at EOF with len
        self.assertEqual(f[len(f)], '')
        self.assertEqual(f.isAtEOF(), True)
        f.close()
        # <<fold
    def testGetItemCurrentPos(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        l = f[2]
        
        self.assertEqual(f.currentPos(), 2)
        # <<fold

    def testFileReadlineBackward(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
     
        f.toEOF()
        l = f.readbackline()
        self.assertEqual(l,"3rd line\n")
        l = f.readbackline()
        self.assertEqual(l,"2nd line\n")
        l = f.readbackline()
        self.assertEqual(l,"1st line\n")
        
        # now the pointer is at begin of file
        self.assertEqual(f.readbackline(), '')
        # <<fold

    def testCurrentLine(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        self.assertEqual(f.currentLine(), '')
        f[1]
        # now we're at line 1
        self.assertEqual(f.currentLine(),"2nd line\n")
        # <<fold
    def testCurrentPos(self): # fold>>
        
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        self.assertEqual(f.currentPos(),-1)
        f[1]
        self.assertEqual(f.currentPos(),1)
        # <<fold

    def testFileSeeks(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        self.assertEqual(f.currentPos(),-1)
        self.assertEqual(f.isAtBOF(), True)
        f.toEOF()
        self.assertEqual( f.currentPos(), 3)
        self.assertEqual( f.isAtEOF(), True)
        f.toBOF()
        self.assertEqual( f.currentPos(), -1)
        self.assertEqual( f.isAtBOF(), True)
        f.toPos(2)
        self.assertEqual( f.currentPos(), 2)
        self.assertEqual( f.isAtPos(2), True)
        # <<fold
    def testSkipLines(self): # fold>>
        "Seeking with relative jumps"
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        self.assertEqual( f.currentPos(), -1)
        f.skipLines(3)
        self.assertEqual( f.currentPos(), 2)
        f.skipLines(-1)
        self.assertEqual( f.currentPos(), 1)
        f.skipLines(10)
        self.assertEqual( f.isAtEOF(), True)
        f.skipLines(-10)
        self.assertEqual( f.isAtBOF(), True)
        # <<fold
    def testOccurrences(self): # fold>>
        "Seeking with relative jumps"
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        f.skipLines(1)
        self.assertEqual(f.isAtPos(0), True)
        self.assertEqual(f.occurrences('line'), [1, 2])
        self.assertEqual(f.isAtPos(0), True)
        f.skipLines(2)
        self.assertEqual(f.isAtPos(2), True)
        self.assertEqual(f.occurrences('line', backward=True),[1, 0])
        self.assertEqual(f.isAtPos(2), True)
        f.toBOF()
        self.assertEqual(f.occurrences('not found'), [])
        # <<fold
    def testFindStringBasic(self): # fold>>
        "Findstring functionality/basic search"
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        self.assertEqual( f.findString("3rd"),"3rd line\n")
        self.assertEqual( f.currentLine(), "3rd line\n")
        f.toEOF()
        self.assertEqual( f.findString("1st", backward=True),"1st line\n")
        self.assertEqual( f.currentLine(),"1st line\n")
        # <<fold 
    def testFindStringCounted(self): # fold>>
        "Findstring functionality/counted search"
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        self.assertEqual(f.findString("line", 2), "2nd line\n")
        self.assertEqual(f.currentLine(), "2nd line\n")
        f.toEOF()
        self.assertEqual(f.findString("line", 2, backward=True), "2nd line\n")
        self.assertEqual(f.currentLine(), "2nd line\n")
    # <<fold
    def testFindStringNotFound(self): # fold>>
        "Findstring functionality/not found case"
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        self.assertEqual(f.findString('notfound'),'')
        self.assertEqual(f.isAtEOF(), True)
        self.assertEqual(f.findString('notfound', backward=True), '')
        self.assertEqual(f.isAtBOF(), True)
        # <<fold 
    def testFindStringCurlineNeverEvaluated(self): # fold>>
        "Findstring functionality/curline never evaluated"
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        f.toPos(0)
        self.assertEqual( f.findString('line'),"2nd line\n")
        self.assertEqual( f.currentLine(), "2nd line\n")
        f.toPos(2)
        self.assertEqual( f.findString('line', backward=True), "2nd line\n")
        self.assertEqual( f.currentLine(), "2nd line\n")
        # <<fold 
    def testRegexpBasic(self): # fold>>
        "Findregexp functionality/basic search"
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        self.assertEqual( f.findRegexp("3rd"), ("3rd line\n",))
        self.assertEqual( f.currentLine(), "3rd line\n")
        f.toEOF()
        self.assertEqual( f.findRegexp("1st", backward=True), ("1st line\n",))
        self.assertEqual( f.currentLine(), "1st line\n")
        # <<fold 
    def testRegexpCounted(self): # fold>>
        "Findregexp functionality/counted search"
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        self.assertEqual(f.findRegexp("line", 2), ("2nd line\n",))
        self.assertEqual(f.currentLine(), "2nd line\n")
        f.toEOF()
        self.assertEqual(f.findRegexp("line", 2, backward=True), ("2nd line\n",))
        self.assertEqual(f.currentLine(),"2nd line\n")
    # <<fold
    def testRegexpNotFound(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        self.assertEqual( f.findRegexp('notfound'), None)
        self.assertEqual( f.isAtEOF(), True)
        self.assertEqual( f.findRegexp('notfound', backward=True), None)
        self.assertEqual( f.isAtBOF(), True)
        # <<fold 
    def testRegexpCurlineNeverEvaluated(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        f.toPos(0)
        self.assertEqual(f.findRegexp('line'), ("2nd line\n",))
        self.assertEqual(f.currentLine(), "2nd line\n")
        f.toPos(2)
        self.assertEqual(f.findRegexp('line', backward=True), ("2nd line\n",))
        self.assertEqual(f.currentLine(),"2nd line\n")
        # <<fold 
    def testRegexp(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"testfile.txt"))
        (line, match) = f.findRegexp('1(.*) line')
        self.assertEqual( line, "1st line\n")
        self.assertEqual( match, 'st')
        # <<fold 

    def testEmptyFileGetItemLen(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"emptytestfile.txt"))
        # has the same length
        self.assertEqual(len(f), 0)
    # <<fold
    def testEmptyFileGetItemOutOfBounds(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"emptytestfile.txt"))
        # move at BOF with big negative num
        self.assertEqual(f[-999999], '')
        self.assertEqual(f.isAtBOF(),True)
        # move at EOF with big positive num
        self.assertEqual(f[9999999], '')
        self.assertEqual(f.isAtEOF(),True)
        # move at BOF with -1
        self.assertEqual(f[-1], '')
        self.assertEqual(f.isAtBOF(),True)
        # move at EOF with len
        self.assertEqual(f[len(f)], '')
        self.assertEqual(f.isAtEOF(),True)
        # <<fold 
    def testEmptyFileReadLine(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"emptytestfile.txt"))
        self.assertEqual(f.readline(),'')
        # <<fold 
    def testEmptyFileReadlineBackward(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"emptytestfile.txt"))
        f.toEOF()
        self.assertEqual(f.readbackline(), '')
            # <<fold 
    def testEmptyFileCurrentLine(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"emptytestfile.txt"))
        self.assertEqual(f.currentLine(), '')
        # <<fold 
    def testEmptyFileCurrentPos(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"emptytestfile.txt"))
        self.assertEqual(f.currentPos(), -1)
        # <<fold 
    def testEmptyFileSeeks(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"emptytestfile.txt"))
        self.assertEqual(f.currentPos(), -1)
        self.assertEqual(f.isAtBOF(), True)
        f.toEOF()
        self.assertEqual(f.currentPos(), 0)
        self.assertEqual(f.isAtEOF(), True)
        f.toBOF()
        self.assertEqual(f.currentPos(), -1)
        self.assertEqual(f.isAtBOF(), True)
    # <<fold
    def testEmptyFileSkipLines(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"emptytestfile.txt"))
        self.assertEqual(f.currentPos(), -1)
        f.skipLines(10)
        self.assertEqual(f.isAtEOF(), True)
        f.skipLines(-10)
        self.assertEqual(f.isAtBOF(), True)
        # <<fold 
    def testEmptyFileOccurrences(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"emptytestfile.txt"))
        self.assertEqual(f.occurrences('not found'), [])
    # <<fold
    def testEmptyFileFindStringNotFound(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"emptytestfile.txt"))
        self.assertEqual( f.findString('notfound'), '')
        self.assertEqual( f.isAtEOF(), True)
        self.assertEqual( f.findString('notfound', backward=True), '')
        self.assertEqual( f.isAtBOF(), True)
    # <<fold
    def testEmptyFileRegexpNotFound(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"emptytestfile.txt"))
        self.assertEqual(f.findRegexp('notfound'), ('', ()))
        self.assertEqual(f.isAtEOF(), True)
        self.assertEqual(f.findRegexp('notfound', backward=True), ('', ()))
        self.assertEqual(f.isAtBOF(), True)
        # <<fold 
    def testEmptyFileRegexpNotFound(self): # fold>>
        f = FileReader.FileReader(os.path.join(moduleDir(),"emptytestfile.txt"))
        self.assertEqual(f.findRegexp('notfound'),None)
        self.assertEqual(f.isAtEOF(), True)
        self.assertEqual(f.findRegexp('notfound', backward=True), None)
        self.assertEqual(f.isAtBOF(), True)
    # <<fold 

if __name__ == '__main__':
    unittest.main()
    
