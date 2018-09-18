from wavemol import parsers


class OutputTokenizer(object):
    def __init__(self):
        self._tokenizer = parsers.Tokenizer(grammar=_fullGrammarOutput())
    
    def tokenize(self, filename):
        return self._tokenizer.tokenize(filename)

def _fullGrammarOutput():
    from wavemol.parsers.dalton import tokentypes
    token_grammar=[ 
            tokentypes.FileHeaderToken,
            tokentypes.CenterOfMassToken,
            tokentypes.IsotopicMassesToken,
            tokentypes.TotalMassToken,
            tokentypes.MomentsOfInertiaToken,
            tokentypes.CartesianCoordinatesToken,
            tokentypes.EndOfOptimizationHeaderToken,
            tokentypes.FinalGeometryEnergyToken,
            tokentypes.GeometryConvergenceNumIterationsToken,
            tokentypes.OptimizationNextGeometryToken,
            tokentypes.OptimizationInfoToken,
            tokentypes.NormalModesEigenvaluesToken,
            tokentypes.AtomsAndBasisSetsToken,
            tokentypes.DipoleMomentToken,
            tokentypes.DipoleMomentComponentsToken,
            tokentypes.FinalGeometryToken,
            tokentypes.HOMOLUMOSeparationToken,
            tokentypes.BondLengthsToken,
            tokentypes.SymmetryToken,
            tokentypes.ResponseHeaderToken,
            tokentypes.FirstHyperpolarizabilityComponentToken,
            tokentypes.SecondHyperpolarizabilityToken,
            tokentypes.LinearResponseToken,
            tokentypes.SevereErrorToken,
            ] 
    return token_grammar
