# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# - Replicates Figure 5: Emotionality in U.S. Congress by Party

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
wd_results = wd + '/3 Replication Package/results/main_paper'  # set the results directory

###################################
#     Upload dataset            ###
###################################

df = pd.read_csv(wd_data + '/main_dataset.csv')

########################################################
#   Timeseries by party - collapsed by congress      ###
#   House only - To see the majorities               ###
########################################################

data = df[df.chamber == 'house']
lab = data[['congress', 'speech_year']].groupby('congress').first().rename(columns={'speech_year': 'labyear'})
data = pd.merge(data, lab, on='congress', how='left')

df1 = data.groupby(['labyear', 'party', 'h_maj_party'])['score'].mean().reset_index()
df1.columns = ['labyear', 'party', 'maj', 'mean']

df2 = data.groupby(['labyear', 'party', 'h_maj_party'])['score'].sem().reset_index()
df2.columns = ['labyear', 'party', 'maj', 'std']

df3 = data.groupby(['labyear', 'party', 'h_maj_party'])['score'].count().reset_index()
df3.columns = ['labyear', 'party', 'maj', 'count']

final = pd.merge(df1, df2, on=['labyear', 'party', 'maj'], how='inner')
final = pd.merge(final, df3, on=['labyear', 'party', 'maj'], how='inner')
final['labyear'] = pd.to_numeric(final['labyear'])

# select categories to plot (women only after 1950s because few obs before)
dem = final[final['party'] == 'Democrat']
rep = final[final['party'] == 'Republican']

rep_maj = [[1918, 1930], [1946, 1948], [1952, 1954], [1994, 2006], [2010, 2014]]
dem_maj = [[1913, 1918], [1930, 1946], [1948, 1952], [1954, 1994], [2006, 2010]]


# Plot

fig = plt.figure(figsize=(30, 15))
ax = plt.axes()
plt.plot(dem['labyear'], dem['mean'], 'k-', label='Democrat Speakers', color='blue')
plt.axvspan(dem_maj[0][0], dem_maj[0][1], facecolor='blue', alpha=0.1, label="Democrat Majority")
plt.fill_between(dem['labyear'], dem['mean']-dem['std'], dem['mean']+dem['std'], facecolor='blue', alpha=0.3)
plt.plot(rep['labyear'], rep['mean'], 'k-', label='Republican Speakers', color='red', linestyle='--')
plt.axvspan(rep_maj[0][0], rep_maj[0][1], facecolor='red', alpha=0.1, label="Republican Majority")
plt.fill_between(rep['labyear'], rep['mean']-rep['std'], rep['mean']+rep['std'], facecolor='red', alpha=0.3)
for i in rep_maj[1:]:
    plt.axvspan(i[0],i[1], facecolor='red', alpha=0.1)
for i in dem_maj[1:]:
    plt.axvspan(i[0],i[1], facecolor='blue', alpha=0.1)
plt.legend(loc='upper left', prop={'size': 24})
plt.xticks(np.arange(1914, 2015, 4), fontsize=20, rotation=90)
plt.yticks(fontsize=20)
plt.grid()

plt.savefig(wd_results + '/fig5.png')



