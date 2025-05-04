# Emotion and Reason in Political Language
# -- Replication Package
# Gennaro and Ash
# 2021

# Description:
# - This code creates the alternative emotionality measure
# based on tfidf socres

###################################
#     Modules                   ###
###################################

import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import glob
from multiprocessing import Pool, freeze_support


###################################
#     Working Directory         ###
###################################

wd_data = '../../../data/3_auxiliary_data'  # set the data directory
wd_results = '../../../results/appendix'  # set the results directory
wd_models = '../../../models'  # set the results directory



###################################
#     Upload everything         ###
###################################

# Upload dicts
cognition = joblib.load(wd_data + '/dictionary_cognition.pkl')
affect = joblib.load(wd_data + '/dictionary_affect.pkl')

# Upload speeches
DATA = glob.glob("speeches_indexed_clean1*.pkl") + \
    glob.glob("speeches_indexed_clean2*.pkl") + \
    glob.glob("speeches_indexed_clean3*.pkl") + \
    glob.glob("speeches_indexed_clean4*.pkl")

text = []
for dataname in DATA:
    d = joblib.load(dataname)
    text = text + d

print('Speeches succesfully uploaded')


###################################
#   Tfidf                       ###
###################################


def dummy_fun(doc):
    return doc


tfidf = TfidfVectorizer(min_df=0.01, max_df=0.9, use_idf=True,
                        analyzer='word', tokenizer=dummy_fun,
                        preprocessor=dummy_fun, token_pattern=None)

text = [a[1] for a in text]

X_tfidf = tfidf.fit_transform(text)

word2tfidf = dict(zip(tfidf.get_feature_names(), tfidf.idf_))


###################################
#     Scoring function          ###
###################################


def find_score(speech):
    a = 0
    c = 0
    lista = [j for j in speech[1] if j in word2tfidf.keys()]
    for w in lista:
        if w in affect:
            a = a + word2tfidf[w]
        elif w in cognition:
            c = c + word2tfidf[w]
        else:
            continue
    return [speech[0], a, c]


def main_function(dataname):
    out = []
    data = joblib.load(dataname)
    for speech in data:
        temp = find_score(speech)
        out.append(temp)
    lab = 'temp_tfidf_' + dataname
    joblib.dump(out, lab)


###################################
#     Multiprocessing           ###
###################################

# Upload speeches
DATA = glob.glob("speeches_indexed_clean1*.pkl") + \
    glob.glob("speeches_indexed_clean2*.pkl") + \
    glob.glob("speeches_indexed_clean3*.pkl") + \
    glob.glob("speeches_indexed_clean4*.pkl")

DATA = [[y] for y in DATA]


def main():
    with Pool(len(DATA)) as pool:
        pool.starmap(main_function, DATA)


if __name__ == "__main__":
    freeze_support()
    main()


###################################
#   Adjust output               ###
###################################

datanames = glob.glob("temp_tfidf_speeches_indexed_clean*.pkl")

data = []
for d in datanames:
    a = joblib.load(d)
    data = data + a
    os.remove(d)


# Calculate final score
data = pd.DataFrame(data)
data.columns = ['title', 'affect_tfidf', 'cognition_tfidf']
data['score_tfidf'] = (data['affect_tfidf']) / (data['cognition_tfidf'])
data['score_tfidf_smooth'] = (1 + data['affect_tfidf']) / (1 + data['cognition_tfidf'])

# Save

joblib.dump(data, 'score_tfidf.pkl')

print('Final score saved')
