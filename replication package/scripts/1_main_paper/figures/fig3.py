# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# - Replicates Figure 3: Emotionality in U.S. Congress by Chamber

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
wd_aux = wd + '/3 Replication Package/data/3_auxiliary_data'

###################################
#     Upload dataset            ###
###################################

df = pd.read_csv(wd_data + '/main_dataset.csv')

# Add demeaned score and adjust come vars
df = df.rename(columns={"topic1_new": "topic_num"})
df['topic_num'] = pd.to_numeric(df['topic_num'], downcast='integer')
df['score_demeaned'] = df['score'] - df['score'].groupby(df['congress']).transform('mean')


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


df = pd.merge(df, topic_labels, on='topic_num', how='left')
df = df[df.speech_year >= 1970]



#####################
#     Panel A     ###
# ###################

data = df

data = data[['topic_broad', 'score_demeaned']]
topics = data.groupby(['topic_broad'])['score_demeaned'].mean().reset_index()
topics.columns = ['topic_broad', 'score']
topics = topics[topics.topic_broad != 'Miscellaneous']

# Plot
topics = topics.sort_values('score', ascending=False)
sorter = topics.topic_broad.to_list()
sorterIndex = dict(zip(sorter, range(len(sorter))))

plt.rcdefaults()
fig, ax = plt.subplots(figsize=(15, 20))
top = topics['topic_broad']
y_pos = np.arange(len(top))
mean = topics['score']
positive = mean > 0
ax.barh(y_pos, mean, align='center',
        color=positive.map({True: 'purple', False: 'darkgreen'}))
ax.set_yticks(y_pos)
ax.set_yticklabels(top)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Average Topic Emotionality', fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=28)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.title('Panel A', fontsize=45, loc="left")
plt.savefig(wd_results + '/fig3a.png')



#####################
#     Panel B     ###
# ###################

data = df

data = data[['party', 'topic_broad', 'score_demeaned']]

topics = data.groupby(['party', 'topic_broad'])['score_demeaned'].mean().reset_index()
topics.columns = ['party', 'topic_broad', 'score']
topics = topics[topics.topic_broad != 'Miscellaneous']
dati1 = topics[topics.party == 'Republican'].sort_values('topic_broad', ascending=False)
dati2 = topics[topics.party == 'Democrat'].sort_values('topic_broad', ascending=False)
uno = list(dati1['score'])
due = list(dati2['score'])

ratio = [(i / j) - 1 for i, j in zip(uno, due)]
dati1['ratio'] = ratio
dati = dati1
del dati['party']
del dati['score']

dati['Rank'] = dati['topic_broad'].map(sorterIndex)
dati = dati.sort_values('Rank', ascending=True)

plt.rcdefaults()
fig, ax = plt.subplots(figsize=(15, 20))
top = dati['topic_broad']
y_pos = np.arange(len(top))
mean = dati['ratio']
positive = mean > 0

ax.barh(y_pos, mean, align='center',
        color=positive.map({True: 'red', False: 'blue'}))
ax.set_yticks(y_pos)
ax.set_yticklabels(top)
ax.invert_yaxis()  # labels read top-to-bottom
ax.yaxis.tick_right()
ax.set_xlabel('Average Topic Emotionality for Republicans over Democrats ', fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=28)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.axvspan(0, 2, facecolor='red', alpha=0.1)
plt.axvspan(-2, 0, facecolor='blue', alpha=0.1)
plt.title('Panel B', fontsize=45, loc="left")
plt.savefig(wd_results + '/fig3b.png')
