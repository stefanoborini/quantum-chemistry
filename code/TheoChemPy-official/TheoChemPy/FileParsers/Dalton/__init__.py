from TheoChemPy.FileParsers import Tokenizer

import Tokens

def tokenizeOutFile(filename):
    token_grammar = Tokens.fullGrammar()
    tokenizer = Tokenizer.Tokenizer(token_grammar)

    return tokenizer.tokenize(filename)

