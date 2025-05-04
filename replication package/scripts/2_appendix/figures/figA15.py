# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# Fig A15

###################################
#     Modules                   ###
###################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random

random.seed(10)


###################################
#     Working Directory         ###
###################################

# indicate here the path to the replication package
wd = "/Users/glgennaro/Dropbox (Personal)/Progetti/Ash_Gennaro/1 EJ paper/EJ-RR/20210282_final_submission"

wd_data = wd + '/3 Replication Package/data/1_main_datasets'  # set the data directory
wd_results = wd + '/3 Replication Package/results/appendix'  # set the results directory
wd_aux = wd + '/3 Replication Package/data/3_auxiliary_data'  # set the data directory

###################################
#     Upload dataset            ###
###################################

df = pd.read_csv(wd_data + '/main_dataset.csv')

###################################
#   Full timeseries             ###
###################################

list(df)
data = df[['topic1_new', 'tenure_start',
           'state', 'speech_year', 'chamber',
           'score', 'affect_d', 'cognition_d',
           'length', 'congress']]

data['affect'] = 1 - data['affect_d']
data['cognition'] = 1 - data['cognition_d']
data['length_quant'] = pd.qcut(data['length'], 10, labels=False)

lab = data[['congress', 'speech_year']].groupby('congress').first().rename(columns={'speech_year': 'labyear'})
data = pd.merge(data, lab, on='congress', how='left')


decades = [[1, 1858, 1868], [2, 1868, 1878], [3, 1878, 1888], [4, 1888, 1898],
           [5, 1898, 1908], [6, 1908, 1918], [7, 1918, 1928], [8, 1928, 1938],
           [9, 1938, 1948], [10, 1948, 1958], [11, 1958, 1968],
           [12, 1968, 1978], [13, 1978, 1988], [14, 1988, 1998],
           [15, 1998, 2008], [16, 2008, 2015]]
DEC = data['speech_year']
for j in range(len(decades)):  # Assign decades to speeches
    i = decades[j]
    dec = int(i[0])
    dec_l = int(i[1])
    dec_u = int(i[2])
    DEC = [dec if dec_l <= int(d) < dec_u else d for d in DEC]
data['decade'] = DEC
del DEC




###########################
#  Correlation by Congress
###########################

sen = data[data.chamber == 'senate']
sen = sen[(sen.topic1_new.isna()) == False]
demean = lambda df: df - df.mean()

sen['affect_dem'] = sen[['topic1_new', 'affect']].groupby(['topic1_new']).transform(demean)
sen['affect_dem'] = sen[['length_quant', 'affect_dem']].groupby(['length_quant']).transform(demean)
sen['cog_dem'] = sen[['topic1_new', 'cognition']].groupby(['topic1_new']).transform(demean)
sen['cog_dem'] = sen[['length_quant', 'cognition']].groupby(['length_quant']).transform(demean)
sen = sen.groupby('labyear')[['affect_dem', 'cog_dem']].corr().iloc[0::2,-1].reset_index()
sen = sen[['labyear', 'cog_dem']]
sen.columns = ['year', 'corr']

house = data[data.chamber == 'house']
house = house[house.topic1_new.isna()==False]
demean = lambda df: df - df.mean()
house['affect_dem'] = house[['topic1_new', 'affect']].groupby(['topic1_new']).transform(demean)
house['affect_dem'] = house[['length_quant', 'affect_dem']].groupby(['length_quant']).transform(demean)
house['cog_dem'] = house[['topic1_new', 'cognition']].groupby(['topic1_new']).transform(demean)
house['cog_dem'] = house[['length_quant', 'cognition']].groupby(['length_quant']).transform(demean)
house = house.groupby('labyear')[['affect_dem','cog_dem']].corr().iloc[0::2,-1].reset_index()
house = house[['labyear', 'cog_dem']]
house.columns = ['year', 'corr']

fig = plt.figure(figsize=(30, 15))
ax = plt.axes()
plt.scatter(sen['year'], sen['corr'], label='Senate', color='r', zorder = 10)
plt.scatter(house['year'], house['corr'], label='House', color='g')
plt.legend(loc='upper left', prop={'size': 24})
plt.xticks(np.arange(1858, 2015, 4), fontsize=20, rotation=90)
plt.yticks(fontsize=20)
plt.grid()
plt.savefig(wd_results + '/figA15.png')


