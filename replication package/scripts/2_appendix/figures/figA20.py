# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# Fig A20


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

###########################################################
#   Timeseries by gender - collapsed by congress        ###
###########################################################

data = df
data['white'] = ''
data['white'][data['race'] == 'White'] = 1
data['white'][data['race'].isin(['African American', 'Asian American', 'Hispanic', 'Native American'])] = 0

lab = data[['congress', 'speech_year']].groupby('congress').first().rename(columns={'speech_year': 'labyear'})
data = pd.merge(data, lab, on='congress', how='left')

df1 = data.groupby(['labyear', 'gender', 'white'])['score'].mean().reset_index()
df1.columns = ['labyear', 'gender', 'white', 'mean']

df2 = data.groupby(['labyear', 'gender', 'white'])['score'].sem().reset_index()
df2.columns = ['labyear', 'gender', 'white', 'std']

df3 = data.groupby(['labyear', 'gender', 'white'])['score'].count().reset_index()
df3.columns = ['labyear', 'gender', 'white', 'count']

final = pd.merge(df1, df2, on=['labyear', 'gender', 'white'], how='inner')
final = pd.merge(final, df3, on=['labyear', 'gender', 'white'], how='inner')
final['labyear'] = pd.to_numeric(final['labyear'])

# select categories to plot (women only after 1950s because few obs before)
femw = final[(final['gender'] == 'F') & (final['white']==1)]
malew = final[(final['gender']=='M') & (final['white']==1)]

femnw = final[(final['gender']=='F') & (final['white']== 0)]
malenw = final[(final['gender']=='M') & (final['white']==0)]

# Plot
fig = plt.figure(figsize=(30, 15))
ax = plt.axes()
plt.plot(femw['labyear'], femw['mean'], 'k-', label='Female White', color='green')
plt.fill_between(femw['labyear'], femw['mean']-femw['std'], femw['mean']+femw['std'], facecolor='green', alpha=0.3)
plt.plot(malew['labyear'], malew['mean'], 'k-', label='Male White', color='blue', linestyle='--')
plt.fill_between(malew['labyear'], malew['mean']-malew['std'], malew['mean']+malew['std'], facecolor='blue', alpha=0.3)
plt.plot(femnw['labyear'], femnw['mean'], 'k-', label='Female Non White', color='purple')
plt.fill_between(femnw['labyear'], femnw['mean']-femnw['std'], femnw['mean']+femnw['std'], facecolor='purple', alpha=0.3)
plt.plot(malenw['labyear'], malenw['mean'], 'k-', label='Male Non White', color='red', linestyle='--')
plt.fill_between(malenw['labyear'], malenw['mean']-malenw['std'], malenw['mean']+malenw['std'], facecolor='red', alpha=0.3)
plt.legend(loc='upper left', prop={'size': 24})
plt.xticks(np.arange(1914, 2014, 4), fontsize=20, rotation=90)
plt.yticks(fontsize=20)
plt.grid()

plt.savefig(wd_results + '/figA20.png')

