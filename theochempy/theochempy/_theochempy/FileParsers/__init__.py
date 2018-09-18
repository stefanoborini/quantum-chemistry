from theochempy._theochempy.FileParsers import Tokenizer

import Tokens

def tokenize(filename):
    token_grammar = Tokens.fullGrammar()
    tokenizer = Tokenizer.Tokenizer(token_grammar)

    return tokenizer.tokenize(filename)

