# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# - Replicates Figure 4: Emotionality by Topic Over Time.

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

df = df[df.congress >= 56]  # Starting on 1900



###################
#     Panel A   ###
###################

data = df[['congress', 'speech_year', 'topic_macro', 'score']]
lab = data[['congress', 'speech_year']].groupby('congress').first().rename(columns={'speech_year': 'labyear'})

data = pd.merge(data, lab, on='congress', how='left')

t1 = data.groupby(['topic_macro', 'labyear'])['score'].mean().reset_index()
t1.columns = ['topic', 'labyear', 'score']
t2 = data.groupby(['topic_macro', 'labyear'])['score'].sem().reset_index()
t2.columns = ['topic', 'labyear', 'score_std']

topics = pd.merge(t1, t2, on=['topic', 'labyear'], how='left')
topics = topics[topics.topic != '']

# Plot
labels = list(set(topics['topic']))
fig, ax = plt.subplots(figsize=(30, 15))
for label in labels:
    x = topics['labyear'][topics.topic == label]  # immigration
    y = topics['score'][topics.topic == label]
    if label=='Economy':
        line1, = ax.plot(x, y, label=label, linewidth=4)
    else:
	    line1, = ax.plot(x, y, label=label)
plt.yticks(fontsize=20)
plt.xticks(np.arange(1900, 2015, 4), fontsize=20, rotation=90)
ax.legend(loc='upper left', prop={'size': 24})
plt.title('Panel A', fontsize=40, loc="left")
plt.grid()
plt.savefig(wd_results + '/fig4a.png')




###################
#     Panel B   ###
###################



data = df[['congress', 'speech_year', 'topic_broad', 'score']]
lab = data[['congress', 'speech_year']].groupby('congress').first().rename(columns={'speech_year': 'labyear'})
data = pd.merge(data, lab, on='congress', how='left')


t1 = data.groupby(['topic_broad', 'labyear'])['score'].mean().reset_index()
t1.columns = ['topic', 'labyear', 'score']
t2 = data.groupby(['topic_broad', 'labyear'])['score'].sem().reset_index()
t2.columns = ['topic', 'labyear', 'score_std']

topics = pd.merge(t1, t2, on=['topic', 'labyear'], how='left')

# Plot
labels = ['Economic Policy', 'Monetary Policy', 'Fiscal Policy']
fig, ax = plt.subplots(figsize=(30, 15))
for l in labels:
	x = topics['labyear'][topics.topic==l]  # immigration
	y = topics['score'][topics.topic==l]
	#s = topics['score_std'][topics.topic==l]
	#ax.fill_between(x, (y-s), (y+s), alpha=.2)
	line1, = ax.plot(x, y, label=l)
plt.yticks(fontsize=20)
plt.title('Panel B', fontsize=40, loc="left")
plt.xticks(np.arange(1900, 2015, 4), fontsize=20, rotation=90)
plt.grid()

ax.legend(loc='upper left', prop={'size': 24})
plt.savefig(wd_results + '/fig4b.png')


