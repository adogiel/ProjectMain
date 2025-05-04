# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# Tab A7

###################################
#     Modules                   ###
###################################

import pandas as pd


###################################
#     Working Directory         ###
###################################

wd = "/Users/glgennaro/Dropbox (Personal)/Progetti/Ash_Gennaro/1 EJ paper/EJ-RR/20210282_final_submission"

wd_data =  wd + '/3 Replication Package/data/1_main_datasets'  # set the data directory
wd_results = wd + '/3 Replication Package/results/appendix'  # set the results directory


###################################
#     Upload dataset            ###
###################################

df = pd.read_csv(wd_data + '/main_dataset.csv', low_memory=False)


#####################################################
# Find top emotional congressmen since 2009   #######
#####################################################

data1 = df[df['speech_year'] >= 2009]
data1 = data1.groupby(['first_name','member', 'state', 'chamber']).agg({'score': 'mean',
                       'title': 'count'}).reset_index()

data1 = data1.sort_values(by=['score'], ascending=False)

# Top-left
topleft = data1[(data1['chamber'] == 'house') & (data1['title'] >= 10)].iloc[:5]
print(topleft)

# Top-Right
topright =data1[(data1['chamber'] == 'senate') & (data1['title'] >= 10)].iloc[:5]
print(topright)


#####################################################
# Find bottom emotional congressmen since 2009   #######
#####################################################

data1 = df[df['speech_year'] >= 2009]
data1 = data1.groupby(['first_name','member', 'state', 'chamber']).agg({'score': 'mean',
                       'title': 'count'}).reset_index()

data1 = data1.sort_values(by=['score'], ascending=True)

# Bottom Left
botleft = data1[(data1['chamber'] == 'house') & (data1['title'] >= 10)].iloc[:5]
print(botleft)

# Bottom Right
botright = data1[(data1['chamber'] == 'senate') & (data1['title'] >= 10)].iloc[:5]
print(botright)

