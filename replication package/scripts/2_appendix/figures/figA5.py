# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# Fig A5

###################################
#     Modules                   ###
###################################

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


###################################
#     Working Directory         ###
###################################

# indicate here the path to the replication package
wd = "/Users/glgennaro/Dropbox (Personal)/Progetti/Ash_Gennaro/1 EJ paper/EJ-RR/20210282_final_submission"

wd_data = wd + '/3 Replication Package/data/1_main_datasets'  # set the data directory
wd_results = wd + '/3 Replication Package/results/appendix'  # set the results directory

###################################
#     Upload dataset            ###
###################################

df = pd.read_csv(wd_data + '/main_dataset.csv')


####################################################
# Emotional states                           #######
####################################################

data1 = df[df['speech_year'] >= 2009]
data1a = data1.groupby(['state'])['score'].mean().reset_index()
data1b = data1.groupby(['state'])['score'].sem().reset_index()
data1b.columns = ['state', 'std1']
data1a.columns = ['state', 'mean1']

data2 = df[df['speech_year'] < 2009]
data2a = data2.groupby(['state'])['score'].sem().reset_index()
data2a.columns = ['state', 'std2']
data2b = data2.groupby(['state'])['score'].mean().reset_index()
data2b.columns = ['state', 'mean2']

final1 = pd.merge(data1a, data1b, on=['state'], how='inner')
final2 = pd.merge(data2a, data2b, on=['state'], how='inner')

final = pd.merge(final1, final2, on=['state'], how='inner')
final = final.sort_values(by=['mean1'], ascending=False)
final['id'] = list(range(len(final)))


# Plot

fig = plt.figure(figsize=(35, 15))
ax = plt.axes()
fig.canvas.draw()
plt.errorbar(final['id'], final['mean1'], final['std1'], linestyle='None',
             marker='D', label='Period 2009-2014')
plt.errorbar(final['id'], final['mean2'], final['std2'], linestyle='None',
             marker='D', label='Period 1858-2008')
ax.set_xticklabels(final['state'])
plt.legend(loc='upper right', prop={'size': 25})
plt.xticks(np.arange(0, len(final['state']), 1), fontsize=20)
plt.yticks(fontsize=20)
plt.grid()

plt.savefig(wd_results + '/figA5.png')

