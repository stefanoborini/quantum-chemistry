# @author Stefano Borini
import os; import sys; script_path=sys.path[0]; sys.path.append(os.path.join(script_path, "../../../"));
import unittest
import tempfile

from theochempy._theochempy.IO import DirWalker

def moduleDir():
    return os.path.dirname(__file__)

    
class TestDirWalker(unittest.TestCase):
    def testDirWalker(self): # fold>>
        d = DirWalker.DirWalker(os.path.join(moduleDir(),"dirwalker-test"))
        
        self.assertEqual(d.__class__, DirWalker.DirWalker)
        # <<fold
    def testTraversal(self):
        d = DirWalker.DirWalker(os.path.join(moduleDir(),"dirwalker-test"))

        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/.svn"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/.svn/all-wcprops"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/.svn/entries"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/.svn/format"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/.svn/prop-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/.svn/props"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/.svn/text-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/.svn/tmp"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/.svn/tmp/prop-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/.svn/tmp/props"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/.svn/tmp/text-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/.svn"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/.svn/all-wcprops"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/.svn/entries"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/.svn/format"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/.svn/prop-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/.svn/props"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/.svn/text-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/.svn/tmp"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/.svn/tmp/prop-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/.svn/tmp/props"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/.svn/tmp/text-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/.svn"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/.svn/all-wcprops"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/.svn/entries"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/.svn/format"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/.svn/prop-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/.svn/props"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/.svn/text-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/.svn/tmp"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/.svn/tmp/prop-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/.svn/tmp/props"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/.svn/tmp/text-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/.svn"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/.svn/all-wcprops"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/.svn/entries"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/.svn/format"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/.svn/prop-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/.svn/props"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/.svn/text-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/.svn/text-base/file1.txt.svn-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/.svn/text-base/file2.txt.svn-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/.svn/text-base/file3.txt.svn-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/.svn/tmp"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/.svn/tmp/prop-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/.svn/tmp/props"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/.svn/tmp/text-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/file1.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/file2.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/file3.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/.svn"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/.svn/all-wcprops"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/.svn/entries"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/.svn/format"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/.svn/prop-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/.svn/props"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/.svn/text-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/.svn/text-base/barfile.txt.svn-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/.svn/text-base/barfile2.txt.svn-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/.svn/text-base/barfile3.txt.svn-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/.svn/text-base/barfile4.mp3.svn-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/.svn/tmp"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/.svn/tmp/prop-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/.svn/tmp/props"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/.svn/tmp/text-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/bar.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/bar.txt/.svn"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/bar.txt/.svn/all-wcprops"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/bar.txt/.svn/entries"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/bar.txt/.svn/format"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/bar.txt/.svn/prop-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/bar.txt/.svn/props"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/bar.txt/.svn/text-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/bar.txt/.svn/tmp"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/bar.txt/.svn/tmp/prop-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/bar.txt/.svn/tmp/props"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/bar.txt/.svn/tmp/text-base"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/barfile.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/barfile2.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/barfile3.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/barfile4.mp3"))
        self.assertRaises(StopIteration, d.next)

    def testTraversalFiltered(self):
        d = DirWalker.DirWalker(os.path.join(moduleDir(),"dirwalker-test"), filter = DirWalker.ExtensionFilter("txt"))

        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/file1.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/file2.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/file3.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/bar.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/barfile.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/barfile2.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/barfile3.txt"))
        self.assertRaises(StopIteration, d.next)

    def testTraversalFiltered2(self):
        d = DirWalker.DirWalker(os.path.join(moduleDir(),"dirwalker-test"), filter = DirWalker.AndFilter(DirWalker.ExtensionFilter("txt"), DirWalker.TypeFilter(DirWalker.TypeFilter.FILE) ))

        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/file1.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/file2.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/baz/baa/moo/file3.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/barfile.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/barfile2.txt"))
        self.assertEqual(d.next(), os.path.join(moduleDir(),"dirwalker-test/foo/barfile3.txt"))
        self.assertRaises(StopIteration, d.next)

        
    
if __name__ == '__main__':
    unittest.main()
    
