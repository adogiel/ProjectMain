# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# Fig A18

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


topic_labels['topic_macro'] = 'Miscellaneous'
topic_labels['topic_macro'].iloc[topic_labels['topic_broad'].isin(['Economic Policy', 'Fiscal Policy', 'Monetary Policy'])] = 'Economy'
topic_labels['topic_macro'].iloc[topic_labels['topic_broad'].isin(['Governance'])] = 'Governance'
topic_labels['topic_macro'].iloc[topic_labels['topic_broad'].isin(['Immigration', 'Social Issues'])] = 'Society'
topic_labels['topic_macro'].iloc[topic_labels['topic_broad'].isin(['Foreign Policy'])] = 'Foreign Affairs'
topic_labels['topic_macro'].iloc[topic_labels['topic_broad'].isin(['Procedure'])] = 'Procedure'
topic_labels['topic_macro'].iloc[topic_labels['topic_broad'].isin(['National Narrative'])] = 'National Narrative'
topic_labels['topic_macro'].iloc[topic_labels['topic_broad'].isin(['Party Politics', 'Tribute'])] = 'Party Politics'


df = pd.merge(df, topic_labels, on='topic_num', how='left')


# Plot

data = df[['congress', 'speech_year', 'topic_num', 'topic_broad', 'topic_macro']].sort_values(by=['congress', 'speech_year'])
lab = data[['congress', 'speech_year']].groupby('congress').first().rename(columns={'speech_year': 'labyear'})
data = pd.merge(data, lab, on='congress', how='left')

del data['congress']
data = data.groupby(['labyear', 'topic_broad']).size().reset_index(name='counts')
data = data.pivot(index='labyear', columns='topic_broad', values='counts')

del data['Miscellaneous']
data = data[data.index>=1900]

# Make the plot
data1 = data
del data1['Procedure'] 
data_perc = data1.divide(data1.sum(axis=1), axis=0)
fig = plt.figure(figsize=(30, 15))
plt.stackplot(data_perc.index,
	          data_perc['Economic Policy'], data_perc['Fiscal Policy'],
	          data_perc['Foreign Policy'], data_perc['Governance'],
	          data_perc['Immigration'], data_perc['Monetary Policy'],
	          data_perc['National Narrative'], data_perc['Party Politics'],
	          data_perc['Social Issues'], data_perc['Tribute'],
	          labels=list(data_perc),
	          colors =['tab:blue', 'tab:orange', 'tab:green', 'tab:red',
	          'tab:purple', 'tab:brown', 'tab:pink', 'tab:grey',
	          'tab:cyan', 'lightgreen'])
plt.legend(loc='upper left', prop={'size': 24})
plt.margins(0,0)
plt.xticks(np.arange(1900, 2014, 4), fontsize=20, rotation=90)
plt.yticks(fontsize=20)
plt.savefig(wd_results + '/figA18.png', dpi=100)


