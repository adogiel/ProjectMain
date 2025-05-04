
# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# - Drop rare words

# NB: currently set up to work on 4 cores


###################################
#     Modules                   ###
###################################

import os
import joblib
from multiprocessing import Pool, freeze_support


###################################
#     Working Directory         ###
###################################

data_c = './data'

###################################
#    Functions                  ###
###################################

os.chdir(data_c)
count = joblib.load('word_counts.pkl')


def select(lista):
    for i in range(len(lista)):
        x = lista[i][0]
        y = lista[i][1]
        y = [w for w in y if count[w] >= 10]
        lista[i] = [x, y]
    return lista


def final_cleaning(dataname):
	data = joblib.load(dataname)
	data = select(data)
	lab = dataname.replace('_temp.pkl', '_clean.pkl')
	joblib.dump(data, lab)


###################################
#      Multiprocessing          ###
###################################

DATI = ['rawspeeches_indexed1_temp.pkl', 'rawspeeches_indexed2_temp.pkl',
        'rawspeeches_indexed3_temp.pkl', 'rawspeeches_indexed4_temp.pkl']


DATI = [[a] for a in DATI]
os.chdir(data_c)

def main():
    with Pool(4) as pool:
        pool.starmap(final_cleaning, DATI)

if __name__ == "__main__":
    freeze_support()
    main()

