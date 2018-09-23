from theochempy._theochempy.FileParsers import Dalton20
from theochempy._theochempy.FileParsers.Dalton20 import Tokens

def getAtomsAndBasisSetsToken(token_list): # fold>>
    tokens = filter(lambda x: x.__class__ == Tokens.AtomsAndBasisSetsToken, token_list)
    if len(tokens) != 1:
        raise Exception("Sorry. Could not find atom and basis set information")
    token = tokens[0]
    if token.basisSet() is None:
        raise Exception("Sorry, only single basis set (BASIS) description are currently supported")
    return token
    # <<fold
def getCartesianCoordinatesToken( token_list): # fold>>
    end_of_optimization = False
    for token in token_list:
        if token.__class__ == Tokens.CartesianCoordinatesToken:
            return token

    return None 
    # <<fold
def getFirstHyperpolarizabilityComponentToken( token_list): # fold>>
    first_hyper_token_list = []
    for token in token_list:
        if token.__class__ == Tokens.FirstHyperpolarizabilityComponentToken:
            first_hyper_token_list.append(token)
    return first_hyper_token_list
    # <<fold
def getSecondHyperpolarizabilityToken( token_list): # fold>>
    second_hyper_token_list = []
    for token in token_list:
        if token.__class__ == Tokens.SecondHyperpolarizabilityToken:
            second_hyper_token_list.append(token)
    return second_hyper_token_list
    # <<fold
def getFinalGeometryToken( token_list): # fold>>
    end_of_optimization = False
    for token in token_list:
        if token.__class__ == Tokens.EndOfOptimizationHeaderToken:
            end_of_optimization = True

        if end_of_optimization:
            if token.__class__ == Tokens.FinalGeometryToken:
                return token

    return None
# <<fold 

