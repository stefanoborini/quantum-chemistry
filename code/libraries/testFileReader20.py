import os
import sys
import unittest
import tempfile
from filereader20 import FileReader

"""
This is a test suite for the FileReader 2.0 class.
"""

class FileReaderTestCase(unittest.TestCase):
    lines = ('1st line\n', '2nd line\n', '3rd line\n')
    
    def setUp(self):
        self.tmpfn = tempfile.mktemp("filereadertest")
        fp = open(self.tmpfn, 'w')
        for line in self.lines:
            fp.write(line)
        fp.close()
        self.f = FileReader(self.tmpfn)
        
    def tearDown(self):
        self.f.close()
        os.unlink(self.tmpfn)

class FileReaderTest1(FileReaderTestCase):
    "Base behaviour tests"
    
    def testGetItemLen(self):
        "Basic behaviour as a list of lines"
        # has the same length
        assert len(self.f) == len(self.lines)
        # has the same lines
        for i in xrange(len(self.lines)):
            assert self.f[i] == self.lines[i]

    def testGetItemOutOfBounds(self):
        "Out of bounds indexes are used to move to EOF/BOF"
        # move at BOF with big negative num
        assert self.f[-999999] == ''
        assert self.f.isAtBOF()
        # move at EOF with big positive num
        assert self.f[9999999] == ''
        assert self.f.isAtEOF()
        # move at BOF with -1
        assert self.f[-1] == ''
        assert self.f.isAtBOF()
        # move at EOF with len
        assert self.f[len(self.f)] == ''
        assert self.f.isAtEOF()
        
    def testGetItemCurrentPos(self):
        "The internal pointer is the last accessed line"
        l = self.f[2]
        # now the pointer is at 2
        assert self.f.currentPos() == 2
        
    def testFileReadLine(self):
        "Readline behaves like a basic file"
        for line in self.lines:
            l = self.f.readline()
            assert l == line
        # now the pointer is at end of file
        assert self.f.readline() == ''
        
    def testFileReadlineBackward(self):
        "Readbackline is like readline but backwards"
        self.f.toEOF()
        # we use a reversed copy of self.lines
        lines = list(self.lines)
        lines.reverse()
        for line in lines:
            l = self.f.readbackline()
            assert l == line
        # now the pointer is at begin of file
        assert self.f.readbackline() == ''
            
    def testCurrentLine(self):
        "Currentline gives the current line"
        # we start a t begin of file, no curline
        assert self.f.currentLine() == ''
        self.f[1]
        # now we're at line 1
        assert self.f.currentLine() == self.lines[1]
        
    def testCurrentPos(self):
        "Currentpos gives the current position"
        # we start a t begin of file
        assert self.f.currentPos() == -1
        self.f[1]
        # now we're at line 1
        assert self.f.currentPos() == 1
        
    def testFileSeeks(self):
        "Seeking with toEOF, toBOF, toPos, and isAt* friends"
        assert self.f.currentPos() == -1
        assert self.f.isAtBOF()
        self.f.toEOF()
        assert self.f.currentPos() == len(self.lines)
        assert self.f.isAtEOF()
        self.f.toBOF()
        assert self.f.currentPos() == -1
        assert self.f.isAtBOF()
        self.f.toPos(2)
        assert self.f.currentPos() == 2
        assert self.f.isAtPos(2)

    def testSkipLines(self):
        "Seeking with relative jumps"
        assert self.f.currentPos() == -1
        self.f.skipLines(3)
        assert self.f.currentPos() == 2
        self.f.skipLines(-1)
        assert self.f.currentPos() == 1
        self.f.skipLines(10)
        assert self.f.isAtEOF()
        self.f.skipLines(-10)
        assert self.f.isAtBOF()
        
    def testOccurrences(self):
        "Seeking with relative jumps"
        self.f.skipLines(1)
        assert self.f.isAtPos(0)
        assert self.f.occurrences('line') == [1, 2]
        assert self.f.isAtPos(0)
        self.f.skipLines(2)
        assert self.f.isAtPos(2)
        assert self.f.occurrences('line', backward=True) == [1, 0]
        assert self.f.isAtPos(2)
        self.f.toBOF()
        assert self.f.occurrences('not found') == []
        

class FileReaderFindStringTest(FileReaderTestCase):
    "Test findString"
    def testFindStringBasic(self):
        "Findstring functionality/basic search"
        assert self.f.findString("3rd") == self.lines[2]
        assert self.f.currentLine() == self.lines[2]
        self.f.toEOF()
        assert self.f.findString("1st", backward=True) == self.lines[0]
        assert self.f.currentLine() == self.lines[0]
        
    def testFindStringCounted(self):
        "Findstring functionality/counted search"
        assert self.f.findString("line", 2) == self.lines[1]
        assert self.f.currentLine() == self.lines[1]
        self.f.toEOF()
        assert self.f.findString("line", 2, backward=True) == self.lines[1]
        assert self.f.currentLine() == self.lines[1]

    def testFindStringNotFound(self):
        "Findstring functionality/not found case"
        assert self.f.findString('notfound') == ''
        assert self.f.isAtEOF()
        assert self.f.findString('notfound', backward=True) == ''
        assert self.f.isAtBOF()
        
    def testFindStringCurlineNeverEvaluated(self):
        "Findstring functionality/curline never evaluated"
        self.f.toPos(0)
        assert self.f.findString('line') == self.lines[1]
        assert self.f.currentLine() == self.lines[1]
        self.f.toPos(2)
        assert self.f.findString('line', backward=True) == self.lines[1]
        assert self.f.currentLine() == self.lines[1]

class FileReaderFindRegExpTest(FileReaderFindStringTest):
    "Test findRegExp"
    
    def setUp(self):
        FileReaderTestCase.setUp(self)
        self.findRegExp = self.f.findRegExp
        
    def testRegexpBasic(self):
        "FindRegExp functionality/basic search"
        assert self.findRegExp("3rd") == (self.lines[2],)
        assert self.f.currentLine() == self.lines[2]
        self.f.toEOF()
        assert self.findRegExp("1st", backward=True) == (self.lines[0],)
        assert self.f.currentLine() == self.lines[0]
        
    def testRegexpCounted(self):
        "FindRegExp functionality/counted search"
        assert self.findRegExp("line", 2) == (self.lines[1],)
        assert self.f.currentLine() == self.lines[1]
        self.f.toEOF()
        assert self.findRegExp("line", 2, backward=True) == (self.lines[1],)
        assert self.f.currentLine() == self.lines[1]

    def testRegexpNotFound(self):
        "FindRegExp functionality/not found case"
        assert self.findRegExp('notfound') == None
        assert self.f.isAtEOF()
        assert self.findRegExp('notfound', backward=True) == None
        assert self.f.isAtBOF()
        
    def testRegexpCurlineNeverEvaluated(self):
        "FindRegExp functionality/curline never evaluated"
        self.f.toPos(0)
        assert self.findRegExp('line') == (self.lines[1],)
        assert self.f.currentLine() == self.lines[1]
        self.f.toPos(2)
        assert self.findRegExp('line', backward=True) == (self.lines[1],)
        assert self.f.currentLine() == self.lines[1]
        
    def testRegexp(self):
        "FindRegExp functionality/search on a real regexp"
        (line, match) = self.findRegExp('1(.*) line')
        assert line == self.lines[0]
        assert match == 'st'

class FileReaderTestEmpty(FileReaderTestCase):
    "Behaviour in case of empty file"
    lines = ()
        
    def testGetItemLen(self):
        "Basic behaviour as a list of lines"
        # has the same length
        assert len(self.f) == 0

    def testGetItemOutOfBounds(self):
        "Out of bounds indexes are used to move to EOF/BOF"
        # move at BOF with big negative num
        assert self.f[-999999] == ''
        assert self.f.isAtBOF()
        # move at EOF with big positive num
        assert self.f[9999999] == ''
        assert self.f.isAtEOF()
        # move at BOF with -1
        assert self.f[-1] == ''
        assert self.f.isAtBOF()
        # move at EOF with len
        assert self.f[len(self.f)] == ''
        assert self.f.isAtEOF()
        
    def testFileReadLine(self):
        "Readline behaves like a basic file"
        assert self.f.readline() == ''
        
    def testFileReadlineBackward(self):
        "Readbackline is like readline but backwards"
        self.f.toEOF()
        assert self.f.readbackline() == ''
            
    def testCurrentLine(self):
        "Currentline gives the current line"
        assert self.f.currentLine() == ''
        
    def testCurrentPos(self):
        "Currentpos gives the current position"
        assert self.f.currentPos() == -1
        
    def testFileSeeks(self):
        "Seeking with toEOF, toBOF, toPos, and isAt* friends"
        assert self.f.currentPos() == -1
        assert self.f.isAtBOF()
        self.f.toEOF()
        assert self.f.currentPos() == len(self.lines)
        assert self.f.isAtEOF()
        self.f.toBOF()
        assert self.f.currentPos() == -1
        assert self.f.isAtBOF()

    def testSkipLines(self):
        "Seeking with relative jumps"
        assert self.f.currentPos() == -1
        self.f.skipLines(10)
        assert self.f.isAtEOF()
        self.f.skipLines(-10)
        assert self.f.isAtBOF()
        
    def testOccurrences(self):
        "Seeking with relative jumps"
        assert self.f.occurrences('not found') == []

    def testFindStringNotFound(self):
        "Findstring functionality/not found case"
        assert self.f.findString('notfound') == ''
        assert self.f.isAtEOF()
        assert self.f.findString('notfound', backward=True) == ''
        assert self.f.isAtBOF()

    def testRegexpNotFound(self):
        "Findregexp functionality/not found case"
        assert self.f.findRegExp('notfound') == None
        assert self.f.isAtEOF()
        assert self.f.findRegExp('notfound', backward=True) == None
        assert self.f.isAtBOF()
    
if __name__ == '__main__':
    unittest.main()
    
# vim: et ts=4 sw=4
