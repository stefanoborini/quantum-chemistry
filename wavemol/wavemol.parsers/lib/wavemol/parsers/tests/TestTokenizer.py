# @author Stefano Borini
import os
import unittest

from wavemol import parsers 

class TokenFoo(object):
    def __init__(self, value):
        self._value = value
    def value(self):
        return self._value
    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()
        try:
            data = line.split(" ")
        except:
            return None

        if data[0] == "foo":
            return cls(data[1])

        return None
            
class TokenBar(object):
    def __init__(self, value):
        self._value = value
    def value(self):
        return self._value
    @classmethod
    def match(cls, reader, previous_tokens):
        line = reader.readline()
        try:
            data = line.split(" ")
        except:
            return None

        if data[0] == "bar":
            return cls(data[1])

        return None

class TestTokenizer(unittest.TestCase):
    def testInit(self): # fold>>
        g = [ TokenFoo, TokenBar ] 
        tokenizer = parsers.Tokenizer(grammar = g)

    def testTokenize(self):
        g = [ TokenFoo, TokenBar ] 
        tokenizer = parsers.Tokenizer(grammar = g)
        tokens = tokenizer.tokenize(os.path.join(os.path.dirname(__file__),"testfiles","test_tokenizer.txt"))
        t = tokens.next()
        self.assertEqual(t.__class__, TokenFoo)
        t = tokens.next()
        self.assertEqual(t.__class__, TokenBar)
        self.assertRaises(StopIteration, tokens.next)

        # <<fold


if __name__ == '__main__':
    unittest.main()
    
