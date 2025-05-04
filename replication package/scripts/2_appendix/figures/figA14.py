# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# Fig A14


###################################
#     Modules                   ###
###################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


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
#     Affect vs Cognition       ###
###################################

df['affect_sim'] = 1 - df['affect_d']
df['cognition_sim'] = 1 - df['cognition_d']

# Affect by year
df1 = df.groupby(['speech_year'])['affect_sim'].mean().reset_index()
df1.columns = ['year', 'mean']
df2 = df.groupby(['speech_year'])['affect_sim'].sem().reset_index()
df2.columns = ['year', 'std']
final = pd.merge(df1, df2, on=['year'], how='inner')
final['year'] = pd.to_numeric(final['year'])


# Cognition by year
df1 = df.groupby(['speech_year'])['cognition_sim'].mean().reset_index()
df1.columns = ['year', 'mean']
df2 = df.groupby(['speech_year'])['cognition_sim'].sem().reset_index()
df2.columns = ['year', 'std']
final2 = pd.merge(df1, df2, on=['year'], how='inner')
final2['year'] = pd.to_numeric(final['year'])


# Time seried of affect vs cognition
fig = plt.figure(figsize=(30, 15))
ax = plt.axes()
plt.plot(final['year'], final['mean'], 'k-', label='Affect', color='purple', linestyle='--')
plt.fill_between(final['year'], final['mean']-final['std'], final['mean']+final['std'], facecolor='purple', alpha=0.3);
plt.plot(final2['year'], final2['mean'], 'k-', label='Cognition', color='darkgreen')
plt.fill_between(final2['year'], final2['mean']-final2['std'], final2['mean']+final2['std'], facecolor='darkgreen', alpha=0.3);
plt.legend(loc='lower right', prop={'size': 24})
plt.xticks(np.arange(1850, 2018, 5), fontsize=20, rotation=90)
plt.yticks(fontsize=20)
plt.grid()

plt.savefig(wd_results + '/figA14.png')

