# Emotion and Reason in Political Language
# -- Replication Package
# Gennaro and Ash
# 2021

# Description:
# - Find length of speeches to add as controls. In particular:
    # 1. length of full speech (without stop words etc-clean)
    # 2. length of dictionary words in speeches
    # 3. length of affect words
    # 4. length ot cognition words


###################################
#     Modules                   ###
###################################

import os
import joblib
import pandas as pd
import glob

###################################
#     Working Directory         ###
###################################

# Set working directory
wd_data = './data/3_auxiliary_data'


###################################
#     Function                  ###
###################################
 
 
### Upload dictionaries
os.chdir(wd_data)
cognition = joblib.load('dictionary_cognition.pkl')
affect = joblib.load('dictionary_affect.pkl')
cognition = set(cognition)
affect = set(affect)
emotions = cognition.union(affect)
del cognition

# Upload pre-processed speeches
DATA = glob.glob("speeches_indexed_clean*.pkl") # upload clean speeches
tot = []
for d in DATA:
    data = joblib.load(d)
    t = []
    for i in range(len(data)):
        x = data[i][0]
        y = data[i][1]
        l1 = len(y)  # all words

        y = [w for w in y if w in emotions]
        l2 = len(y)

        y = [w for w in y if w in affect]
        l3 = len(y)  # only affect Words

        f = [x, l1, l2, l3]

        t = t + f
    tot = tot + t


tot = pd.DataFrame(tot)
tot.columns = ['title', 'length', 'len_dict', 'len_affect']
tot['len_cognition'] = tot['len_dict'].sub(tot['len_affect'], axis = 0)

joblib.dump(tot, 'length.pkl')
