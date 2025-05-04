
# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# - Find absolute frequencies of vocabulary words in corpus
# - Find absolute frequencies of affect and cognition words in corpus
# - Find SIF frequencies across all corpus


###################################
#     Modules                   ###
###################################

import os
import joblib
from collections import Counter


###################################
#     Working Directory         ###
###################################

data_c = './data'
wd_dir = './data/word_frequencies/'

####################
#   Word counts   ##
####################

DATI = ['rawspeeches_indexed1_n_temp.pkl', 'rawspeeches_indexed2_n_temp.pkl',
        'rawspeeches_indexed3_n_temp.pkl', 'rawspeeches_indexed4_n_temp.pkl']

def find_frequencies(dataset_name):
	data = joblib.load(dataset_name)
	data = [a[1] for a in data]
	data = [a for b in data for a in b]
	data = Counter(data)

os.chdir(data_c)

freqs = Counter()
for dataset_name in DATI:
	temp = find_frequencies(dataset_name)
	freqs = sum([freqs, temp], Counter())

joblib.dump(freqs, wd_dir + 'word_counts.pkl')


###############################
#   Count dictionary words   ##
###############################

# Counts for dictionary words
affect = joblib.load('dictionary_affect.pkl')
cognition = joblib.load('dictionary_cognition.pkl')

a = [[i, freqs[i]] for i in affect]
c = [[i, freqs[i]] for i in cognition]a = sorted(a, key = lambda x: x[1], reverse=True)
c = sorted(c, key = lambda x: x[1], reverse=True)a = [[i[0], '(' + str(i[1])+'),'] for i in a]
c = [[i[0], '(' + str(i[1])+'),'] for i in c]a1 = ' '.join(str(r) for v in a for r in v)
c1 = ' '.join(str(r) for v in c for r in v)os.chdir(results)

with open(wd_dir + "affect_words.txt", "w") as output:
    output.write(str(a1))
 
with open(wd_dir + "cog_words.txt", "w") as output:
    output.write(str(c1))


#########################
#   Weightes Frequences #
#########################

l = sum(freqs.values())

a = 0.001
for key in freqs.keys():
    freqs[key] = a / (a + (freqs[key] / l))

joblib.dump(freqs, wd_dir + 'word_freqs.pkl')
