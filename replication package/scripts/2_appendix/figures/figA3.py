# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description:
# Fig A3: Desity of emotionality by decade

###################################
#     Modules                   ###
###################################

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

###################################
#   Density by decade           ###
###################################

decades = [[1, 1858, 1868], [2, 1868, 1878], [3, 1878, 1888], [4, 1888, 1898],
           [5, 1898, 1908], [6, 1908, 1918], [7, 1918, 1928], [8, 1928, 1938],
           [9, 1938, 1948], [10, 1948, 1958], [11, 1958, 1968],
           [12, 1968, 1978], [13, 1978, 1988], [14, 1988, 1998],
           [15, 1998, 2008], [16, 2008, 2015]]


DEC = df['speech_year']
for j in range(len(decades)):  # Assign decades to speeches
    i = decades[j]
    dec = int(i[0])
    dec_l = int(i[1])
    dec_u = int(i[2])
    DEC = [dec if dec_l <= int(d) < dec_u else d for d in DEC]
df['decade'] = DEC
del DEC



figure, axes = plt.subplots(nrows=4, ncols=4, constrained_layout=True)
plt.setp(axes, 
	    ylim = [0, 2.5] , 
        yticks=[1, 2],
        yticklabels=['1', '2'],
        xlim = [0, 2], 
        xticks=[0.5, 1, 1.5],
        xticklabels=['0.5', '1', '1.5'])
axes = axes.ravel()
for i in range(16):
	dec = i + 1
	axes[i].hist(df['score'][df['decade']==dec], bins=20, density=True)
	axes[i].set_title(str(decades[i][1]) + '-' + str(decades[i][2]-1))
figure.tight_layout()
plt.savefig(wd_results + '/figA3.png')


