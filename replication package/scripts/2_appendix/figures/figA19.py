# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# Fig A19

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
#     Upload topic labels       ###
###################################

topic_labels = pd.read_csv(wd_aux + '/topics_numbers.csv', header=None)
topic_labels = list(topic_labels[0])
topic_labels = [[topic_labels[x], topic_labels[x + 1], topic_labels[x + 2]]
                for x in range(0, len(topic_labels) - 1, 3)]
topic_labels = pd.DataFrame(topic_labels, columns=['topic_num', 'topic', 'theme'])
topic_labels['topic_num'] = pd.to_numeric(topic_labels['topic_num'], downcast='integer')
topic_labels[['topic_broad', 'topic_detail']] = topic_labels['topic'].str.split(' - ', 1, expand=True)


topic_labels['topic_macro'] = ''
topic_labels['topic_macro'].iloc[topic_labels['topic_broad'].isin(['Economic Policy', 'Fiscal Policy', 'Monetary Policy'])] = 'Economy'
topic_labels['topic_macro'].iloc[topic_labels['topic_broad'].isin(['Governance'])] = 'Governance'
topic_labels['topic_macro'].iloc[topic_labels['topic_broad'].isin(['Immigration', 'Social Issues'])] = 'Society'
topic_labels['topic_macro'].iloc[topic_labels['topic_broad'].isin(['Foreign Policy'])] = 'Foreign Affairs'
topic_labels['topic_macro'].iloc[topic_labels['topic_broad'].isin(['Procedure'])] = 'Procedure'
topic_labels['topic_macro'].iloc[topic_labels['topic_broad'].isin(['National Narrative'])] = 'National Narrative'
topic_labels['topic_macro'].iloc[topic_labels['topic_broad'].isin(['Party Politics', 'Tribute'])] = 'Party Politics'

df = df.rename(columns={"topic1_new": "topic_num"})
df['topic_num'] = pd.to_numeric(df['topic_num'], downcast='integer')
df = pd.merge(df, topic_labels, on='topic_num', how='left')

data = df
data = data[data.topic_macro!='Procedure']


d1 = data.groupby(['chamber', 'speech_year'])['score'].mean().reset_index()
d1.columns = ['chamber', 'speech_year', 'mean']
d2 = data.groupby(['chamber', 'speech_year'])['score'].sem().reset_index()
d2.columns = ['chamber', 'speech_year', 'std']
final = pd.merge(d1, d2, on=['chamber', 'speech_year'], how='inner')
final['speech_year'] = pd.to_numeric(final['speech_year'])
final = final.sort_values(by=['speech_year'])
sen = final[final['chamber'] == 'senate']
con = final[final['chamber'] == 'house']

# Plot
fig = plt.figure(figsize=(30, 15))
ax = plt.axes()
plt.plot(sen['speech_year'], sen['mean'], label='Senate', color='r', zorder = 10)
plt.fill_between(sen['speech_year'], sen['mean']-sen['std'], sen['mean']+sen['std'], facecolor='r', alpha=0.3, zorder = 10)
plt.plot(con['speech_year'], con['mean'], label='House', color='g')

plt.fill_between(con['speech_year'], con['mean']-con['std'], con['mean']+con['std'], facecolor='g', alpha=0.3, zorder = 10)
ax.axvspan(1861, 1865, alpha=0.1, color='red', zorder = 1)
plt.text(1860, 1.05,'Civil War', fontsize=25) # bbox=dict(facecolor='white', edgecolor='none'))
ax.axvspan(1914, 1918, alpha=0.1, color='red', zorder = 1)
plt.text(1913, 1.05,'WW1', fontsize=25) # bbox=dict(facecolor='white', edgecolor='none'))
ax.axvspan(1939, 1945, alpha=0.1, color='red', zorder = 1)
plt.text(1939, 1.1,'WW2', fontsize=25) #bbox=dict(facecolor='white', edgecolor='none'))
ax.axvspan(1979, 1986, alpha=0.1, color='red', zorder = 0)
ax.axvspan(1986, 2014, alpha=0.2, color='red', zorder = 0)

plt.legend(loc='upper left', prop={'size': 24})
plt.xticks(np.arange(1858, 2015, 5), fontsize=20, rotation=90)
plt.yticks(fontsize=20)
plt.text(1987, 1.15,'C-SPAN2', fontsize=25) #, bbox=dict(facecolor='white', edgecolor='none'))
plt.text(1977, 1.1,'C-SPAN1', fontsize=25) #, bbox=dict(facecolor='white', edgecolor='none'))
plt.grid()
plt.savefig(wd_results + '/figA19.png')

