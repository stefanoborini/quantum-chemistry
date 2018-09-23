from wavemol import parsers

class ListOutputTokenizer(object):
    def __init__(self):
        self._tokenizer = parsers.Tokenizer(grammar=_fullGrammarOutput())
    
    def tokenize(self, filename):
        return self._tokenizer.tokenize(filename)

class InputTokenizer(object):
    def __init__(self):
        self._tokenizer = parsers.Tokenizer(grammar=_fullGrammarInput())
    
    def tokenize(self, filename):
        return self._tokenizer.tokenize(filename)

class TSAnalysisOutputTokenizer(object):
    def __init__(self):
        self._tokenizer = parsers.Tokenizer(grammar=_fullGrammarTSAnalysisOutput())
    
    def tokenize(self, filename):
        return self._tokenizer.tokenize(filename)

class UDCAnalysisOutputTokenizer(object):
    def __init__(self):
        self._tokenizer = parsers.Tokenizer(grammar=_fullGrammarUDCAnalysisOutput())
    
    def tokenize(self, filename):
        return self._tokenizer.tokenize(filename)

def _fullGrammarOutput():
    from wavemol.parsers.grrm import tokentypes
    token_grammar=[ 
            tokentypes.HeaderDissociatedToken,
            tokentypes.HeaderEquilibriumToken,
            tokentypes.HeaderTransitionToken,
            tokentypes.StructureHeaderToken,
            tokentypes.GeometryToken,
            tokentypes.EnergyToken,
            tokentypes.SpinToken,
            tokentypes.ZPVEToken,
            tokentypes.NormalModesToken,
            tokentypes.ConnectionToken,
            tokentypes.DissociationFragmentsToken,
            ] 
    return token_grammar


def _fullGrammarInput():
    from wavemol.parsers.grrm import tokentypes
    token_grammar=[ 
            tokentypes.CommandDirectiveToken,
            tokentypes.InputGeometryToken,
            tokentypes.OptionsHeaderToken,
            tokentypes.NRunOptionToken,
            ] 
    return token_grammar

def _fullGrammarTSAnalysisOutput():
    from wavemol.parsers.grrm import tokentypes
    token_grammar=[ 
                tokentypes.OptimizationHeaderToken,
                tokentypes.OptimizationIterationToken,
                tokentypes.OptimizationFinalStructureToken,
                tokentypes.NormalModesTSToken,
                tokentypes.MinimumPointFoundHeaderToken,
                tokentypes.InitialStructureToken,
                tokentypes.IRCHeaderToken,
                tokentypes.EnergyProfileToken,
                tokentypes.BackwardIRCHeaderToken,
                tokentypes.ForwardIRCHeaderToken,
                tokentypes.IRCFollowingResultsToken,
                tokentypes.IRCStepToken,
                tokentypes.DCReachedToken,
                tokentypes.EQWithinStepsizeHeaderToken,
                tokentypes.GradientVectorToken,
            ] 
    return token_grammar

def _fullGrammarUDCAnalysisOutput():
    from wavemol.parsers.grrm import tokentypes
    token_grammar=[ 
                tokentypes.IRCHeaderToken,
                tokentypes.InitialStructureToken,
                tokentypes.GradientVectorToken,
                tokentypes.NormalModesTSToken,
                tokentypes.SteepestDescentHeaderToken,
                tokentypes.IRCStepToken,
                tokentypes.EQWithinStepsizeHeaderToken,
                tokentypes.OptimizationHeaderToken,
                tokentypes.OptimizationIterationToken,
                tokentypes.OptimizationFinalStructureToken,
                tokentypes.MinimumPointFoundHeaderToken,
                tokentypes.EnergyProfileToken,
                tokentypes.DownhillWalkingResultToken,
            ] 
    return token_grammar

