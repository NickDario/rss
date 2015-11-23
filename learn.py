import numpy


string = 'You get used to feeling scared'

# data = [(string, truth), ...]
def predict(data);
    feats = _extractFeatures(data[0])


def _extractFeatures(string):
    features = []
    # 
    # METHOD 1: custom features
    # 
    # 1. process text - apply negative to following word
    #
    # percent adj   positive 
    # percent nouns positive 
    # percent verbs positive 
    #
    # percent adj   negative
    # percent nouns negative
    # percent verbs negative 
    # 
    # percent words positive
    # percent words negative
    # 
    # avg positive word position
    # avg negative word position
    #

    # 
    # METHOD 2: dynamic text
    # 
    # 1. Add all words.lemma_ to dictionary if not already in it.
    # 2. Apply weights to words
    # 
    # 


    return features