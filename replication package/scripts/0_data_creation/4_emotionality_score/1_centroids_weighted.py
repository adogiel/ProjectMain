# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# - Find the document vectors for the cognition and affcet dictionaries
# - These centroids are SIF weighted averages

###################################
#     Modules                   ###
###################################

import os
import joblib
from gensim.models import Word2Vec
import numpy as np

###################################
#   Working directory           ###
###################################

wd_data = './data'
wd_models = './models'

###################################
# Upload all elements           ###
###################################

os.chdir(wd_data)
cognition = joblib.load('dictionaries/dictionary_cognition.pkl')
affect = joblib.load('dictionaries/dictionary_affect.pkl')

# Upload word vectors
w2v = Word2Vec.load(wd_models + '/w2v-vectors_8_300.pkl', mmap='r')
word_vectors = w2v.wv

# Upload word frequencies
freqs = joblib.load('word_frequencies/word_freqs.pkl')

###################################
# Find the centroid             ###
###################################

def findcentroid(text, model):
    vecs = [model.wv[w] * freqs[w] for w in text if w in model.wv]
    vecs = [v for v in vecs if len(v) > 0]
    centroid = np.mean(vecs, axis=0)
    centroid = centroid.reshape(1, -1)
    return centroid


c_affect = findcentroid(affect, w2v)
c_cognition = findcentroid(cognition, w2v)


###################################
# Save                          ###
###################################

os.chdir(wd_data)
joblib.dump(c_affect, '3_auxiliary_data/affect_centroid.pkl')
joblib.dump(c_cognition, '3_auxiliary_data/cog_centroid.pkl')
