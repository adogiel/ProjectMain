# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# Plot Emotionality and setiment

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

###################################
#     Upload dataset            ###
###################################

df = pd.read_csv(wd_data + '/main_dataset.csv')


########################################
# Matrix emotionality - sentiment      #
########################################

x = np.array(df['score'])
y = np.array(df['sentiment'])

fig = plt.figure(figsize=(20, 20))
plt.scatter(x, y, s=0.01)
plt.xlabel("Cognition - Emotion", fontsize=20)
plt.ylabel("Negative - Positive Sentiment", fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.savefig(wd_results + '/figA2.png')


# Correlation coefficient

#pd.Series(x).corr(pd.Series(y), method='pearson')

#y = np.array(df['sentiment_vader'])
#pd.Series(x).corr(pd.Series(y), method='pearson')
