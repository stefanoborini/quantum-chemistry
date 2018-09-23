from theochempy._theochempy.IO import FileReader

class Tokenizer:
    def __init__(self, token_grammar):
        self._token_grammar = token_grammar

    def tokenize(self,filename):
        reader = FileReader.FileReader(filename)
        token_list = []
        while not reader.isAtEOF():
            token = self._resolveNextToken(reader)
            if token is None:
                reader.readline()
            else:
                token_list.append(token)
        return token_list
    
    def _resolveNextToken(self,reader):
        for token_class in self._token_grammar:
            token = token_class.match(reader)
            if token is not None:
                return token
        
        return None


