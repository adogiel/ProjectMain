# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# Fig A12

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


#####################################
# Trends in the Google dataset    ###
#####################################

# Normalize the score
df['speech_year'] = pd.to_numeric(df['speech_year'])

df1 = df.groupby(['speech_year'])['google'].mean().reset_index()
df1.columns = ['year', 'google']
df1 = df1[df1['year'] >= 1900]

# Plot
fig = plt.figure(figsize=(30, 15))
ax = plt.axes()
plt.plot(df1['year'], df1['google'], 'k-', label='Emotionality in Google Books', color='green')
plt.legend(loc='upper right', prop={'size': 20})
plt.xticks(np.arange(1900, 2018, 5), fontsize=20, rotation=90)
plt.yticks(fontsize=20)
plt.grid()
plt.savefig(wd_results + '/figA12.png')

