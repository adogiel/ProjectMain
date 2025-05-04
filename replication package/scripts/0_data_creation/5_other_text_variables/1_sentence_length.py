# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash
# 2021

# Description:
# - Extract sentences from the corpus
# - Calculate average sentence length in speech



###################################
#     Modules                   ###
###################################

import os
from gensim.summarization.textcleaner import get_sentences
import joblib
from multiprocessing import Pool, freeze_support
import pandas as pd

###################################
#     Working Directory         ###
###################################

# Set working directory
data_c = './data'

# Upload speeches
DATI = ['rawspeeches_indexed1.pkl', 'rawspeeches_indexed2.pkl',
        'rawspeeches_indexed3.pkl', 'rawspeeches_indexed4.pkl']


###################################
#     Function                  ###
###################################
 
def sentence_length(dataname):
    data = joblib.load(dataname)
    lab = 'len_sent_temp_' + dataname
    len_sentences = []
    for doc in data:
        sentences = get_sentences(doc[1])
        lst = [len(s.split()) for s in sentences]
        if len(lst) == 0:
            continue
        else:
            media = sum(lst) / len(lst)
            len_sentences.append([doc[0], media])
    joblib.dump(len_sentences, lab)


###################################
#     Multiprocessing           ###
###################################

DATASET = [[a] for a in DATI]
os.chdir(data_c)


def main():
    with Pool(4) as pool:
        pool.starmap(sentence_length, DATASET)


if __name__ == "__main__":
    freeze_support()
    main()


###################################
#     Save                      ###
###################################

DATI = ['len_sent_temp_' + str(a) for a in DATI]

os.chdir(data_c)
df = []
for data in DATI:
	d = joblib.load(data)
	df.append(d)
	os.remove(data)

df = [a for l in df for a in l]
df = pd.DataFrame(df, columns = ['title', 'sent_length'])
joblib.dump(df, 'sent_length.pkl')
