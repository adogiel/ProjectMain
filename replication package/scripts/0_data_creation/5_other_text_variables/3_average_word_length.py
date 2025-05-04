# Emotion and Reason in Political Language
# -- Replication Package
# Gennaro and Ash
# 2021

# Description:
# - Find average word length in speech


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
 
os.chdir(wd_data)
DATA = glob.glob("speeches_indexed_clean*.pkl") # upload clean speeches

tot = []
for d in DATA:
    data = joblib.load(d)
    t = []
    for i in range(len(data)):
        x = data[i][0]
        y = data[i][1]
        if len(y)>0:
            l = sum(map(len, y)) / len(y)
        else:
            l = 0
        f = [x, l]
        t.append(f)
    tot = tot + t

tot = pd.DataFrame(tot)
tot.columns = ['title', 'word_length']

joblib.dump(tot, 'word_length.pkl')
