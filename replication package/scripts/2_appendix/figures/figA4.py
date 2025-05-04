# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# Fig A4: Desity of emotionality score vs. count method 

###################################
#     Modules                   ###
###################################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


###################################
#     Working Directory         ###
###################################

wd = "/Users/glgennaro/Dropbox (Personal)/Progetti/Ash_Gennaro/1 EJ paper/EJ-RR/20210282_final_submission"

wd_data = wd + '/3 Replication Package/data/1_main_datasets'  # set the data directory
wd_results = wd + '/3 Replication Package/results/appendix'  # set the results directory

###################################
#     Upload dataset            ###
###################################

df = pd.read_csv(wd_data + '/main_dataset.csv', low_memory=False)


#######################################
#   Plots of embeddings vs tfidf    ###
#######################################

temp = df.score_tfidf_smooth
temp = temp[(temp < np.percentile(temp, 90))]
fig = plt.hist(temp, bins=100)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('')
plt.ylabel('')
plt.title('Distribution of the TfIdf-based score')
plt.savefig(wd_results + '/figA4a.png')
plt.clf()

temp = df.affect_tfidf
temp = temp[(temp < np.percentile(temp, 90))]
fig = plt.hist(temp, bins=100)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('')
plt.ylabel('')
plt.title('Distribution of the TfIdf Affect score')
plt.savefig(wd_results + '/figA4b.png')
plt.clf()

temp = df.cognition_tfidf
temp = temp[(temp < np.percentile(temp, 90))]
fig = plt.hist(temp, bins=100)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('')
plt.ylabel('')
plt.title('Distribution of the TfIdf Congition score')
plt.savefig(wd_results + '/figA4c.png')
plt.clf()


fig = plt.hist(df.score, bins=100)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('')
plt.ylabel('')
plt.title('Distribution of the Emotionality score')
plt.savefig(wd_results + '/figA4d.png')
plt.clf()

temp = 1 - df.affect_d
fig = plt.hist(temp, bins=100)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('')
plt.ylabel('')
plt.title('Distribution of the Affect score')
plt.savefig(wd_results + '/figA4e.png')
plt.clf()

temp = 1 - df.cognition_d
fig = plt.hist(temp, bins=100)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('')
plt.ylabel('')
plt.title('Distribution of the Cognition score')
plt.savefig(wd_results + '/figA4f.png')
plt.clf()



