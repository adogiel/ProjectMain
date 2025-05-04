# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# Fig A6 

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
#   Full timeseries - tfidf     ###
###################################

df['score'] = (1 + df['affect_tfidf']) / (1 + df['cognition_tfidf'])

d1 = df.groupby(['chamber', 'speech_year'])['score'].mean().reset_index()
d1.columns = ['chamber', 'speech_year', 'mean']
d2 = df.groupby(['chamber', 'speech_year'])['score'].sem().reset_index()
d2.columns = ['chamber', 'speech_year', 'std']
final = pd.merge(d1, d2, on=['chamber', 'speech_year'], how='inner')
final['speech_year'] = pd.to_numeric(final['speech_year'])
final = final.sort_values(by=['speech_year'])
sen = final[final['chamber'] == 'senate']
con = final[final['chamber'] == 'house']



# Plot
fig = plt.figure(figsize=(30, 15))
ax = plt.axes()

# Senate
plt.plot(sen['speech_year'], sen['mean'], label='Senate', color='r', zorder = 10)
plt.fill_between(sen['speech_year'], sen['mean']-sen['std'], sen['mean']+sen['std'], facecolor='r', alpha=0.3, zorder = 10)

# House
plt.plot(con['speech_year'], con['mean'], label='House', color='g')
plt.fill_between(con['speech_year'], con['mean']-con['std'], con['mean']+con['std'], facecolor='g', alpha=0.3, zorder = 10)

# Periods
ax.axvspan(1861, 1865, alpha=0.1, color='red', zorder = 1)
plt.text(1860,0.98,'Civil War', fontsize=25)
ax.axvspan(1914, 1918, alpha=0.1, color='red', zorder = 1)
plt.text(1913,0.99,'WW1', fontsize=25) 
ax.axvspan(1939, 1945, alpha=0.1, color='red', zorder = 1)
plt.text(1939, 1.02,'WW2', fontsize=25) 
ax.axvspan(1979, 1986, alpha=0.1, color='red', zorder = 0)
ax.axvspan(1986, 2015, alpha=0.2, color='red', zorder = 0)
plt.legend(loc='upper left', prop={'size': 24})
plt.xticks(np.arange(1858, 2015, 5), fontsize=20, rotation=90)
plt.yticks(fontsize=20)
plt.text(1987,1.1,'C-SPAN2', fontsize=25) 
plt.text(1977,1.07,'C-SPAN1', fontsize=25)
plt.grid()

plt.savefig(wd_results + '/figA6.png')




