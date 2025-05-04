
# Emotion and Reason in Political LanguageL: Replication Package
# Gennaro and Ash

# Description: 
# - Extract documents from their original zip folder
# - Filter out procedural speeches
# - Filter out legislation
# - Clean text spelling


###################################
#     Modules                   ###
###################################

from zipfile import ZipFile
from glob import glob
import os
import shutil
from os import listdir
import pandas as pd
import time
import zipfile
import joblib
from collections import defaultdict
import multiprocessing
import re
import joblib

###################################
#   Working directory           ###
###################################

data_c = './data'  # Temporary data folder
wd_raw = './data/segmented'  # Raw data folder


###################################
#   Extract titles and          ###
#   Drop procedural speeches    ###
###################################

os.chdir(wd_raw)  # Here is where the corpus is

archive1 = ZipFile('hein.zip', 'r')
l = archive1.namelist()
l = [item for item in l if item.endswith('.txt')]
# length: 7724090

archive2 = ZipFile('gpo.zip', 'r')
g = archive2.namelist()
g = [item for item in g if item.endswith('.txt')]
# Length: 1045059

# Eliminate double titles
a = ['/'.join(x.split('/')[1:]) for x in l]
b = ['/'.join(x.split('/')[1:]) for x in g]
c = list(set(b) - set(a))
c = ['gpo/' + x for x in c]  # Final from gpo

del a
del b
del g

print('Titles have been extracted. Length: {}'.format(len(l) + len(c)))


###################################
#   Extract files from path     ###
###################################

data = []

for item in l:
    x = archive1.read(item)
    y = x.decode('utf-8', 'ignore')
    data.append([item, y])


for item in c:
    x = archive2.read(item)
    y = x.decode('utf-8', 'ignore')
    data.append([item, y])

del l
del x
del y
del item
del c

print('Speeches have been extracted. Data length is {}'.format(len(data)))


###################################
#   Clean the set of speeches   ###
###################################

# Eliminate amendments by dropping speeches with indicators
amendment = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)', '(h)', '(i)', '(j)', '(k)', '(l)', '(m)', '(n)', '(o)',
    '(p)', '(q)', '(r)', '(s)', '(t)', '(u)', '(v)', '(w)', '(y)', '(x)', '(z)', '(A)', '(B)', '(C)', '(D)', '(E)',
     '(F)', '(G)', '(H)', '(I)', '(J)', '(K)', '(L)', '(M)', '(N)', '(O)', '(P)', '(Q)', '(R)', '(S)', '(T)', '(U)',
     '(V)', '(W)', '(Y)', '(X)', '(Z)', '(ii)', '(iii)', '(iv)', '(vi)', '(vii)', '(viii)', '(ix)']


def amend(lista):
    lista = [sa for sa in lista if not any(sb in sa[1] for sb in amendment)]
    return lista

data = amend(data)
print('Amendements eliminated. Data length is {}'.format(len(data)))

# Drop empty speeches
def dropnull(lista):
    a = [row for row in lista if len(row[1].split())>0]
    return a


data = dropnull(data)

print('Empty speeches have been eliminated. Data length is {}'.format(len(data)))


###################################
#   Save raw speeches           ###
###################################

data_raw = [a[1] for a in data]

os.chdir(data_c)

joblib.dump(data_raw, 'rawspeeches.pkl')
del data_raw


###################################
#   Cleaning                    ###
###################################

# Eliminate \n
def cleaning1(lista):
    a = [[row[0], row[1].replace('\n', ' ')] for row in lista]
    return a

def cleaning2(lista):
    a = [[row[0], re.sub(r'(?<=[.,])(?=[^\s])', r' ', row[1])] for row in lista]
    return a

def cleaning3(lista):
    a = [[row[0], re.sub(r"-\s", "", row[1])] for row in lista]
    return a

def cleaning4(lista):
    a = [[row[0], row[1].replace("\\", "")] for row in lista]
    return a

def dropnull(lista):
    a = [row for row in lista if len(row[1].split())>0]
    return a

data = cleaning1(data)
data = cleaning2(data)
data = cleaning3(data)
data = cleaning4(data)

data = dropnull(data)

print('Text has been cleaned. Data length is {}'.format(len(data)))

###################################
#   Save clean speeches         ###
###################################

data_id1 = data[:int(len(data)/4)]
data_id2 = data[int(len(data)/4): int(2*len(data)/4)]
data_id3 = data[int(2*len(data)/4):int(3*len(data)/4)]
data_id4 = data[int(3*len(data)/4):]

os.chdir(data_c)
joblib.dump(data_id1, 'rawspeeches_indexed1_n.pkl')
joblib.dump(data_id2, 'rawspeeches_indexed2_n.pkl')
joblib.dump(data_id3, 'rawspeeches_indexed3_n.pkl')
joblib.dump(data_id4, 'rawspeeches_indexed4_n.pkl')
