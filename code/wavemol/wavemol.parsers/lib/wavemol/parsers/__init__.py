from wavemol.core import io

class Tokenizer(object):
    def __init__(self, grammar):
        self._grammar = grammar

    def tokenize(self,filename):
        reader = io.FileReader(filename)
        token_list = []
        while not reader.isAtEOF():
            token = self._tryResolveToken(reader, token_list)
            if token is None:
                reader.readline()
            else:
                token_list.append(token)
                yield token
        raise StopIteration
    
    def _tryResolveToken(self,reader, token_list ):
        original_pos = reader.currentPos()
        for token_class in self._grammar:
            token = token_class.match(reader, token_list)
            if token is not None:
                return token
            else:
                reader.toPos(original_pos)
        
        return None

    def grammar(self):
        return grammar
