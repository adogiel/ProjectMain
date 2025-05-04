# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# Fig A16

###################################
#     Modules                   ###
###################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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





################################################################
#     Most Emotional Topics overall  - demeaned, details     ###
################################################################

data = df[['topic_num', 'topic', 'topic_broad', 'score_demeaned']]

t1 = data.groupby(['topic_num', 'topic', 'topic_broad'])['score_demeaned'].mean().reset_index()
t1.columns = ['topic_num', 'topic', 'topic_broad', 'score']
t2 = data.groupby(['topic_num', 'topic', 'topic_broad'])['score_demeaned'].sem().reset_index()
t2.columns = ['topic_num', 'topic', 'topic_broad', 'score_std']

topics = pd.merge(t1, t2, on=['topic_num', 'topic', 'topic_broad'])
topics = topics[topics.topic != 'Miscellaneous']


# Plot 
topics = topics.sort_values('score', ascending=False)
plt.rcdefaults()
fig, ax = plt.subplots(figsize=(15, 24))
top = topics['topic']
y_pos = np.arange(len(top))
mean = topics['score']
ax.barh(y_pos, mean, align='center')
ax.set_yticks(y_pos)
ax.set_yticklabels(top)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Emotionality', fontsize=24)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.tight_layout()
plt.savefig(wd_results + '/figA16.png', dpi=100)

