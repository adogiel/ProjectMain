# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# Fig A10

###################################
#     Modules                   ###
###################################

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

###################################
#   Full timeseries             ###
###################################

df['sent_length'] = df['sent_length'] / max(df['sent_length'])

df1 = df.groupby(['speech_year'])['sent_length'].mean().reset_index()
df1.columns = ['year', 'sent_length_mean']

df2 = df.groupby(['speech_year'])['sent_length'].sem().reset_index()
df2.columns = ['year', 'sent_length_std']


final = pd.merge(df1, df2, on=['year'], how='inner')

final['year'] = pd.to_numeric(final['year'])

fig = plt.figure(figsize=(30, 15))
ax = plt.axes()
plt.plot(final['year'], final['sent_length_mean'], 'k-', label='Sentence Length', color='red')
plt.fill_between(final['year'], final['sent_length_mean']-final['sent_length_std'], final['sent_length_mean']+final['sent_length_std'], facecolor='red', alpha=0.3)
plt.legend(loc='upper left', prop={'size': 24})
plt.xticks(np.arange(1850, 2018, 5), fontsize=20, rotation=90)
plt.yticks(fontsize=20)
plt.grid()

plt.savefig(wd_results + '/figA10.png')



