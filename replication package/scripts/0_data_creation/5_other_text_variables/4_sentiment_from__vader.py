# Emotion and Reason in Political Language
# -- Replication Package
# Gennaro and Ash
# 2021

# Description:
# - Calculate speech sentiment with vader

###################################
#     Modules                   ###
###################################

import os
import joblib
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer


###################################
#     Working Directory         ###
###################################

# Set working directory
wd_data = './data/3_auxiliary_data'


###################################
#     Main                      ###
###################################

sid = SentimentIntensityAnalyzer()

def sent(lista):
    pol = []
    for i in range(len(lista)):
        x = lista[i][0]
        y = lista[i][1]
        p = sid.polarity_scores(y).get('compound', None)
        pol.append([x, p])
    return pol


DATA = ['rawspeeches_indexed1.pkl',
        'rawspeeches_indexed2.pkl',
        'rawspeeches_indexed3.pkl',
        'rawspeeches_indexed4.pkl']

os.chdir(wd_data)

s = []
for d in DATA:
    data = joblib.load(d)
    s1 = sent(data)
    s = s + s1

s = pd.DataFrame(s)
s.columns = ['title', 'sentiment_vader']

joblib.dump(s, 'sentiment_vader.pkl')
