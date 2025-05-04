# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# Fig A8


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
#   Plot                        ###
###################################

df = pd.read_csv(wd_aux + '/emotionality_score_res_demo.csv')

sen = df[df['house'] == 0]
con = df[df['house'] == 1]

# Plot
fig = plt.figure(figsize=(30, 15))
ax = plt.axes()
plt.plot(sen['speech_year'], sen['score_mean'], label='Senate', color='r', zorder = 10)
plt.plot(con['speech_year'], con['score_mean'], label='House', color='g')
plt.plot(sen['speech_year'], sen['res_mean'], label='Senate - Residualized', color='r', linestyle='--', zorder = 10)
plt.plot(con['speech_year'], con['res_mean'], label='House - Residualized', color='g', linestyle='--')
plt.legend(loc='upper left', prop={'size': 24})
plt.xticks(np.arange(1913, 2015, 5), fontsize=20, rotation=90)
plt.yticks(fontsize=20)
plt.grid()
plt.savefig(wd_results + '/figA8.png')


