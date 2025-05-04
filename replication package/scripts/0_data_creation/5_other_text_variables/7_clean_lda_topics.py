# Emotion and Reason in Political Language
# -- Replication Package
# Gennaro and Ash
# 2021

# Description:
# Clean topic labels


###################################
#     Modules                   ###
###################################

import os
import joblib
import pandas as pd


###################################
#     Working Directory         ###
###################################

wd_data = './data/3_auxiliary_data'

topic = pd.read_csv(wd_data + '/20210119_corp_congress_gpo_lda_topics_gpo_and_hein_128_mallet.csv')
topic = topic[['file_name', 'lda_topics_gpo_and_hein_128_mallet']]
topic.columns = ['title', 'topic']


topic2 = pd.read_csv('topics/20210119_corp_congress_hein_lda_topics_gpo_and_hein_128_mallet.csv')
topic2 = topic2[['file_name', 'lda_topics_gpo_and_hein_128_mallet']]
topic2.columns = ['title', 'topic']

topic = pd.concat([topic, topic2], axis=0)
del topic2

print('Topic uploaded')


# Drop NAs
topic.dropna(subset=["topic"], inplace=True)
topic = topic[topic['topic'] != "{}"]
# length 8 255 178

# RIPRENDI DA QUI
# Split topic lable from topic probability
temp_t = topic.loc[:, 0:84:2]
temp_p = topic.loc[:, 1:85:2]
temp_t.columns = range(0, len(list(temp_t)))
temp_p.columns = range(0, len(list(temp_p)))
# 8 255 178

# Find max probability
temp_p = temp_p.apply(pd.to_numeric)
probs_top1 = temp_p.max(axis=1)
# 8 255 178

# Find colnumber that correspond to max prob
vec = temp_p.idxmax(axis=1)
vec = [int(i) for i in vec]
# 8 255 178

topic_top1 = [temp_t.iloc[r, int(vec[r])]
              for r in range(0, len(temp_t))]


print('top topics selected')

#print('Verify if true: {}'.format(len(topic) == len(topic_top1)))

final = pd.DataFrame(list(zip(topic['title'], topic_top1, probs_top1)),
	                    columns=['title', 'topic1_new', 'topic_prob1_new'])

joblib.dump(final, 'topics_top2_lda.pkl')

