# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# - Model training


###################################
#     Modules                   ###
###################################

import os
import joblib
from gensim.models import Word2Vec


wd_data = './data'
wd_model = './models/'


###################################
#     Upload speeches           ###
###################################

os.chdir(wd_data)

DATI = ['sentences_indexed1.pkl', 'sentences_indexed2.pkl',
        'sentences_indexed3.pkl', 'sentences_indexed4.pkl']

dataset = []
for dataname in DATI:
	data = joblib.load(dataname)
	dataset.append(data)

###################################
#    Model training             ###
###################################

w2v = Word2Vec(dataset,  # iterator that loops over tokenized sentences
               workers=8,  # Number of threads to run in parallel
               size=300,  # Word vector dimensionality
               min_count=10,  # Minimum word count
               window = 8, # Context window size - how many words to use as a context
               sample = 1e-3, # Downsample setting for frequent words
               iter = 10 # epochs
               )

w2v.init_sims(replace=True)

# Save
w2v.save(wd_model + 'w2v-vectors_8_300.pkl')

